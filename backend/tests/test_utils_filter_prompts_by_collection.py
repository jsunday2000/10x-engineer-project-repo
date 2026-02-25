"""Unit tests for filter_prompts_by_collection utility."""

from dataclasses import dataclass
from time import perf_counter
from typing import Optional

import pytest

from app.utils import filter_prompts_by_collection


@dataclass(frozen=True)
class MockPrompt:
    """Minimal prompt-like object for utility testing."""

    id: str
    collection_id: Optional[str]


def test_filter_prompts_by_collection_empty_input_returns_empty_new_list() -> None:
    """Return an empty list and preserve immutability for empty input."""
    prompts: list[MockPrompt] = []

    result = filter_prompts_by_collection(prompts, "col-1")

    assert result == []
    assert len(result) == 0
    assert result is not prompts


def test_filter_prompts_by_collection_no_matches_returns_empty_new_list() -> None:
    """Return no prompts when collection_id does not match any items."""
    prompts = [
        MockPrompt(id="p1", collection_id="col-a"),
        MockPrompt(id="p2", collection_id="col-b"),
    ]
    original_snapshot = list(prompts)

    result = filter_prompts_by_collection(prompts, "col-z")

    assert len(result) == 0
    assert result == []
    assert result is not prompts
    assert prompts == original_snapshot


def test_filter_prompts_by_collection_all_match_returns_all_in_order() -> None:
    """Return all prompts in original order when every item matches."""
    prompts = [
        MockPrompt(id="p1", collection_id="col-a"),
        MockPrompt(id="p2", collection_id="col-a"),
        MockPrompt(id="p3", collection_id="col-a"),
    ]
    original_snapshot = list(prompts)

    result = filter_prompts_by_collection(prompts, "col-a")

    assert len(result) == 3
    assert result == prompts
    assert [prompt.id for prompt in result] == ["p1", "p2", "p3"]
    assert result is not prompts
    assert prompts == original_snapshot


def test_filter_prompts_by_collection_some_match_returns_only_matches() -> None:
    """Return only matching prompts and preserve input list."""
    prompts = [
        MockPrompt(id="p1", collection_id="col-a"),
        MockPrompt(id="p2", collection_id="col-b"),
        MockPrompt(id="p3", collection_id="col-a"),
        MockPrompt(id="p4", collection_id="col-c"),
    ]
    original_snapshot = list(prompts)

    result = filter_prompts_by_collection(prompts, "col-a")

    assert len(result) == 2
    assert result == [prompts[0], prompts[2]]
    assert [prompt.id for prompt in result] == ["p1", "p3"]
    assert result is not prompts
    assert prompts == original_snapshot


def test_filter_prompts_by_collection_excludes_none_collection_ids() -> None:
    """Exclude prompts that have collection_id set to None."""
    prompts = [
        MockPrompt(id="p1", collection_id=None),
        MockPrompt(id="p2", collection_id="col-a"),
        MockPrompt(id="p3", collection_id=None),
    ]
    original_snapshot = list(prompts)

    result = filter_prompts_by_collection(prompts, "col-a")

    assert len(result) == 1
    assert result == [prompts[1]]
    assert all(prompt.collection_id == "col-a" for prompt in result)
    assert result is not prompts
    assert prompts == original_snapshot


def test_filter_prompts_by_collection_preserves_duplicate_prompts() -> None:
    """Preserve duplicates when the same prompt appears multiple times."""
    duplicate_prompt = MockPrompt(id="p1", collection_id="col-a")
    prompts = [duplicate_prompt, duplicate_prompt, MockPrompt(id="p2", collection_id="col-b")]
    original_snapshot = list(prompts)

    result = filter_prompts_by_collection(prompts, "col-a")

    assert len(result) == 2
    assert result == [duplicate_prompt, duplicate_prompt]
    assert result[0] is result[1] is duplicate_prompt
    assert result is not prompts
    assert prompts == original_snapshot


def test_filter_prompts_by_collection_large_list_performance_sanity() -> None:
    """Handle a large list quickly enough for a sanity-level performance check."""
    prompts = [
        MockPrompt(id=f"p-{index}", collection_id="target" if index % 3 == 0 else "other")
        for index in range(100_000)
    ]
    original_snapshot = list(prompts)

    start = perf_counter()
    result = filter_prompts_by_collection(prompts, "target")
    elapsed = perf_counter() - start

    assert len(result) == 33_334
    assert all(prompt.collection_id == "target" for prompt in result)
    assert result is not prompts
    assert prompts == original_snapshot
    assert elapsed < 1.5


def test_filter_prompts_by_collection_is_case_sensitive() -> None:
    """Match collection IDs using exact, case-sensitive comparison."""
    prompts = [
        MockPrompt(id="p1", collection_id="COL-A"),
        MockPrompt(id="p2", collection_id="col-a"),
    ]
    original_snapshot = list(prompts)

    result = filter_prompts_by_collection(prompts, "col-a")

    assert len(result) == 1
    assert result == [prompts[1]]
    assert result is not prompts
    assert prompts == original_snapshot


@pytest.mark.parametrize(
    "prompts, collection_id, expected_exception",
    [
        (None, "col-a", TypeError),
        ([object()], "col-a", AttributeError),
    ],
)
def test_filter_prompts_by_collection_invalid_types_raise(
    prompts: object,
    collection_id: object,
    expected_exception: type[Exception],
) -> None:
    """Raise clear Python errors for unsupported runtime input types."""
    with pytest.raises(expected_exception):
        filter_prompts_by_collection(prompts, collection_id)
