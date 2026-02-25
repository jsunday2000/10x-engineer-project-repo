"""Unit tests for search_prompts utility."""

from dataclasses import dataclass
from typing import Optional

import pytest

from app.utils import search_prompts


@dataclass(frozen=True)
class MockPrompt:
    """Minimal prompt-like object used for utility tests."""

    title: str
    description: Optional[str]


def _assert_new_list_and_input_unchanged(
    prompts: list[MockPrompt],
    original_snapshot: list[MockPrompt],
    result: list[MockPrompt],
) -> None:
    """Assert result immutability guarantees for search utility."""
    assert result is not prompts
    assert prompts == original_snapshot


def test_search_prompts_empty_input_returns_empty_new_list() -> None:
    """Return an empty list for empty input without mutating input list."""
    prompts: list[MockPrompt] = []
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "api")

    assert result == []
    assert len(result) == 0
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_case_insensitive_matching_title_and_description() -> None:
    """Match query in title/description regardless of text casing."""
    prompts = [
        MockPrompt(title="API Checklist", description="General notes"),
        MockPrompt(title="Deploy Guide", description="Includes Api rollout plan"),
        MockPrompt(title="Unrelated", description="No keyword"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "aPi")

    assert len(result) == 2
    assert result == [prompts[0], prompts[1]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_uses_substring_matching() -> None:
    """Match partial substrings in title/description."""
    prompts = [
        MockPrompt(title="integration testing", description=None),
        MockPrompt(title="Unit", description="Contains integ details"),
        MockPrompt(title="Other", description="No match"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "integ")

    assert len(result) == 2
    assert result == [prompts[0], prompts[1]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_handles_none_description_branch() -> None:
    """Safely skip description matching when description is None."""
    prompts = [
        MockPrompt(title="No hit", description=None),
        MockPrompt(title="Keyword in title", description=None),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "keyword")

    assert len(result) == 1
    assert result == [prompts[1]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_handles_empty_description_branch() -> None:
    """Treat empty description string as non-match unless title matches."""
    prompts = [
        MockPrompt(title="No match", description=""),
        MockPrompt(title="Keyword title", description=""),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "keyword")

    assert len(result) == 1
    assert result == [prompts[1]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_with_empty_query_returns_all_prompts_in_order() -> None:
    """Return all prompts when query is empty string."""
    prompts = [
        MockPrompt(title="", description=None),
        MockPrompt(title="Alpha", description=""),
        MockPrompt(title="Beta", description="Something"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "")

    assert len(result) == 3
    assert result == prompts
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_query_with_whitespace_matches_literal_whitespace_substring() -> None:
    """Match query containing spaces as a normal substring."""
    prompts = [
        MockPrompt(title="API review", description=None),
        MockPrompt(title="API-review", description=None),
        MockPrompt(title="Other", description="api review checklist"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "api review")

    assert len(result) == 2
    assert result == [prompts[0], prompts[2]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_no_matches_returns_empty_new_list() -> None:
    """Return empty list when no prompt contains the query."""
    prompts = [
        MockPrompt(title="Alpha", description="One"),
        MockPrompt(title="Beta", description="Two"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "zzz")

    assert len(result) == 0
    assert result == []
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_all_match_preserves_input_order() -> None:
    """Return all matching prompts in original order."""
    prompts = [
        MockPrompt(title="api a", description=None),
        MockPrompt(title="b", description="api b"),
        MockPrompt(title="API c", description="misc"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "api")

    assert len(result) == 3
    assert result == prompts
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_some_match_preserves_input_order() -> None:
    """Return only matching subset while preserving relative order."""
    prompts = [
        MockPrompt(title="alpha", description=None),
        MockPrompt(title="api-first", description=None),
        MockPrompt(title="beta", description="contains api"),
        MockPrompt(title="gamma", description=None),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "api")

    assert len(result) == 2
    assert result == [prompts[1], prompts[2]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_preserves_duplicate_prompts() -> None:
    """Keep duplicates in result when duplicated prompt entries match."""
    duplicate = MockPrompt(title="api", description="same")
    prompts = [duplicate, duplicate, MockPrompt(title="other", description=None)]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "api")

    assert len(result) == 2
    assert result == [duplicate, duplicate]
    assert result[0] is result[1] is duplicate
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_with_special_characters_query() -> None:
    """Support literal substring search for special characters."""
    prompts = [
        MockPrompt(title="Use C++ templates", description=None),
        MockPrompt(title="Use C#", description="No plus signs"),
        MockPrompt(title="Other", description="c++ examples"),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "c++")

    assert len(result) == 2
    assert result == [prompts[0], prompts[2]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_title_empty_string_behavior() -> None:
    """Handle prompts with empty title correctly."""
    prompts = [
        MockPrompt(title="", description="contains api"),
        MockPrompt(title="", description=None),
        MockPrompt(title="non-empty", description=None),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, "api")

    assert len(result) == 1
    assert result == [prompts[0]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_query_whitespace_only() -> None:
    """Treat whitespace-only query as normal substring search."""
    prompts = [
        MockPrompt(title="has space", description=None),
        MockPrompt(title="nospace", description="has a space"),
        MockPrompt(title="nospace", description=None),
    ]
    original_snapshot = list(prompts)

    result = search_prompts(prompts, " ")

    assert len(result) == 2
    assert result == [prompts[0], prompts[1]]
    _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)


def test_search_prompts_invalid_query_type_raises_attribute_error() -> None:
    """Raise a clear runtime error for unsupported query type."""
    prompts = [MockPrompt(title="api", description=None)]

    with pytest.raises(AttributeError):
        search_prompts(prompts, None)  # type: ignore[arg-type]


try:
    from hypothesis import given
    from hypothesis import strategies as st

    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis is not installed")
def test_search_prompts_property_matches_reference_filter() -> None:
    """Match reference behavior for randomized prompt/query combinations."""

    @given(
        prompts=st.lists(
            st.builds(
                MockPrompt,
                title=st.text(max_size=20),
                description=st.one_of(st.none(), st.text(max_size=20)),
            ),
            max_size=40,
        ),
        query=st.text(max_size=10),
    )
    def run_property_test(prompts: list[MockPrompt], query: str) -> None:
        original_snapshot = list(prompts)

        expected = [
            prompt
            for prompt in prompts
            if query.lower() in prompt.title.lower()
            or (prompt.description and query.lower() in prompt.description.lower())
        ]

        result = search_prompts(prompts, query)

        assert result == expected
        _assert_new_list_and_input_unchanged(prompts, original_snapshot, result)

    run_property_test()
