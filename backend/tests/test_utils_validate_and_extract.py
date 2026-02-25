"""Unit tests for validate_prompt_content and extract_variables utilities."""

from dataclasses import dataclass
from datetime import datetime, timedelta
import re

import pytest

from app.utils import (
    extract_variables,
    filter_prompts_by_collection,
    search_prompts,
    sort_prompts_by_date,
    validate_prompt_content,
)


@dataclass(frozen=True)
class PromptLike:
    """Minimal prompt-like model for utility smoke coverage."""

    title: str
    description: str | None
    collection_id: str | None
    created_at: datetime


class TestValidatePromptContent:
    """Tests for prompt content validation utility."""

    def test_none_input_returns_false(self) -> None:
        """Return False when content is None."""
        assert validate_prompt_content(None) is False  # type: ignore[arg-type]

    def test_empty_string_returns_false(self) -> None:
        """Return False when content is empty."""
        assert validate_prompt_content("") is False

    def test_whitespace_only_returns_false(self) -> None:
        """Return False when content contains only whitespace."""
        assert validate_prompt_content("   \t\n  ") is False

    def test_exactly_nine_characters_after_strip_returns_false(self) -> None:
        """Return False for stripped length of 9."""
        assert validate_prompt_content("  123456789  ") is False

    def test_exactly_ten_characters_after_strip_returns_true(self) -> None:
        """Return True for stripped length of 10 (boundary)."""
        assert validate_prompt_content("  1234567890  ") is True

    def test_more_than_ten_characters_returns_true(self) -> None:
        """Return True when stripped length is greater than 10."""
        assert validate_prompt_content("01234567890") is True

    def test_leading_and_trailing_whitespace_is_ignored(self) -> None:
        """Apply length check to stripped content, not raw content."""
        assert validate_prompt_content("   valid text length   ") is True

    def test_unicode_characters_supported(self) -> None:
        """Handle unicode content correctly."""
        assert validate_prompt_content("你好世界你好世界你好") is True

    def test_newlines_and_tabs_supported(self) -> None:
        """Handle newline and tab whitespace around valid content."""
        assert validate_prompt_content("\n\t1234567890\t\n") is True

    def test_very_large_string_returns_true(self) -> None:
        """Handle very large valid input efficiently."""
        assert validate_prompt_content("a" * 100_000) is True


class TestExtractVariables:
    """Tests for template variable extraction utility."""

    def test_no_variables_returns_empty_list(self) -> None:
        """Return empty list when no template variables are present."""
        assert extract_variables("No placeholders here.") == []

    def test_one_variable(self) -> None:
        """Extract one variable token."""
        assert extract_variables("Hello {{name}}") == ["name"]

    def test_multiple_variables(self) -> None:
        """Extract multiple variables in order."""
        assert extract_variables("{{first}} and {{second}} then {{third}}") == [
            "first",
            "second",
            "third",
        ]

    def test_duplicate_variables_preserved(self) -> None:
        """Preserve duplicates in extraction order."""
        assert extract_variables("{{name}} {{name}} {{name}}") == ["name", "name", "name"]

    def test_variables_with_underscores(self) -> None:
        """Match variable names with underscores."""
        assert extract_variables("{{user_name}} {{account_id}}") == ["user_name", "account_id"]

    def test_variables_with_numbers(self) -> None:
        """Match variable names containing digits."""
        assert extract_variables("{{var1}} {{x2y3}}") == ["var1", "x2y3"]

    def test_variables_with_uppercase_letters(self) -> None:
        """Match variable names containing uppercase letters."""
        assert extract_variables("{{UserName}} {{API_KEY}}") == ["UserName", "API_KEY"]

    def test_mixed_valid_and_invalid_patterns(self) -> None:
        """Return only valid {{\\w+}} matches from mixed input."""
        content = "{{valid}} {{invalid-name}} {{also_valid2}} {{ space }} {{_ok}}"
        assert extract_variables(content) == ["valid", "also_valid2", "_ok"]

    def test_nested_braces(self) -> None:
        """Allow inner valid token extraction even within extra braces."""
        assert extract_variables("{{{{name}}}}") == ["name"]

    def test_incomplete_braces(self) -> None:
        """Ignore incomplete brace patterns."""
        content = "{{name} {name}} {{name {{other}}"
        assert extract_variables(content) == ["other"]

    def test_special_characters_inside_braces_not_matched(self) -> None:
        """Ignore placeholders with non-word characters."""
        content = "{{first-name}} {{email@domain}} {{price$}} {{ok_name}}"
        assert extract_variables(content) == ["ok_name"]

    def test_adjacent_variables(self) -> None:
        """Extract adjacent variables without separators."""
        assert extract_variables("{{a}}{{b}}{{c}}") == ["a", "b", "c"]

    def test_variables_with_surrounding_whitespace_not_matched(self) -> None:
        """Ignore placeholders with internal surrounding whitespace."""
        content = "{{ name}} {{name }} {{ name }} {{name}}"
        assert extract_variables(content) == ["name"]

    def test_large_input_string(self) -> None:
        """Extract variables correctly from large inputs."""
        content = ("x" * 10_000) + " {{v1}} middle {{v2}} " + ("y" * 10_000)
        assert extract_variables(content) == ["v1", "v2"]

    @pytest.mark.parametrize(
        "content, expected",
        [
            ("{{}}", []),
            ("{{ }}", []),
            ("{{-}}", []),
            ("{{a-b}}", []),
            ("{{a.b}}", []),
            ("{{a b}}", []),
            ("{{123}}", ["123"]),
            ("{{_}}", ["_"]),
            ("{{a}}{{}}{{b}}", ["a", "b"]),
            ("{{a}}}}", ["a"]),
            ("{{{{a}}", ["a"]),
        ],
    )
    def test_fuzz_style_malformed_brace_patterns(
        self,
        content: str,
        expected: list[str],
    ) -> None:
        """Fuzz-style malformed inputs to verify robust regex matching."""
        assert extract_variables(content) == expected


class TestAdditionalUtilsCoverage:
    """Minimal smoke tests to complete utility module coverage."""

    def test_sort_prompts_by_date_descending_and_ascending(self) -> None:
        """Sort prompts by created_at in both directions."""
        base = datetime(2024, 1, 1, 0, 0, 0)
        prompts = [
            PromptLike("t1", None, "c1", base + timedelta(seconds=20)),
            PromptLike("t2", None, "c1", base + timedelta(seconds=10)),
            PromptLike("t3", None, "c1", base + timedelta(seconds=30)),
        ]

        descending = sort_prompts_by_date(prompts, descending=True)
        ascending = sort_prompts_by_date(prompts, descending=False)

        assert [prompt.title for prompt in descending] == ["t3", "t1", "t2"]
        assert [prompt.title for prompt in ascending] == ["t2", "t1", "t3"]
        assert descending is not prompts
        assert ascending is not prompts

    def test_filter_prompts_by_collection_smoke(self) -> None:
        """Filter prompts by exact collection_id."""
        now = datetime(2024, 1, 1, 0, 0, 0)
        prompts = [
            PromptLike("a", None, "x", now),
            PromptLike("b", None, "y", now),
            PromptLike("c", None, "x", now),
        ]

        result = filter_prompts_by_collection(prompts, "x")

        assert [prompt.title for prompt in result] == ["a", "c"]
        assert result is not prompts

    def test_search_prompts_smoke_description_none_and_non_none(self) -> None:
        """Cover search matching in title and description branches."""
        now = datetime(2024, 1, 1, 0, 0, 0)
        prompts = [
            PromptLike("API title", None, "c", now),
            PromptLike("Other", "contains api", "c", now),
            PromptLike("Nope", None, "c", now),
        ]

        result = search_prompts(prompts, "api")

        assert [prompt.title for prompt in result] == ["API title", "Other"]
        assert result is not prompts


try:
    from hypothesis import given
    from hypothesis import strategies as st

    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis is not installed")
def test_extract_variables_property_returns_only_word_tokens() -> None:
    """Ensure all extracted values satisfy \\w+ and preserve order by construction."""

    separator = st.text(
        alphabet=st.characters(blacklist_characters="{}"),
        max_size=5,
    )

    @given(
        names=st.lists(
            st.from_regex(r"\w+", fullmatch=True),
            min_size=0,
            max_size=25,
        ),
        sep=separator,
    )
    def run_property_test(names: list[str], sep: str) -> None:
        content = sep.join(f"{{{{{name}}}}}" for name in names)
        result = extract_variables(content)

        assert result == names
        assert all(re.fullmatch(r"\w+", item) for item in result)

    run_property_test()


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis is not installed")
def test_validate_prompt_content_property_matches_reference_logic() -> None:
    """Validate result matches direct reference logic for random strings."""

    @given(st.text())
    def run_property_test(content: str) -> None:
        expected = bool(content and content.strip() and len(content.strip()) >= 10)
        assert validate_prompt_content(content) is expected

    run_property_test()
