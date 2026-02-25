"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.

    Sorts a list of prompts by their created_at timestamp in either ascending
    or descending order. Does not modify the original list.

    Args:
        prompts: List of Prompt objects to sort.
        descending: If True (default), sorts newest first (descending order).
            If False, sorts oldest first (ascending order).

    Returns:
        A new sorted list of prompts. Original list remains unchanged.

    Example:
        >>> prompts = [prompt1, prompt2, prompt3]
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=True)
        >>> sorted_prompts[0].created_at >= sorted_prompts[-1].created_at
        True
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts to only those in a specific collection.

    Returns a new list containing only prompts whose collection_id matches
    the provided collection_id. Prompts with no collection_id are excluded.

    Args:
        prompts: List of Prompt objects to filter.
        collection_id: The UUID of the collection to filter by.

    Returns:
        A new list containing only prompts in the specified collection.
        Original list remains unchanged. Returns empty list if no matches found.

    Example:
        >>> all_prompts = [prompt1, prompt2, prompt3]
        >>> collection_prompts = filter_prompts_by_collection(all_prompts, "col-123")
        >>> all(p.collection_id == "col-123" for p in collection_prompts)
        True
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title and description using case-insensitive matching.

    Searches through prompt titles and descriptions for the given query string.
    The search is case-insensitive and uses substring matching. Only considers
    non-null descriptions.

    Args:
        prompts: List of Prompt objects to search through.
        query: Search query string. Will be converted to lowercase for matching.

    Returns:
        A new list of prompts where the query appears in title or description.
        Original list remains unchanged. Returns empty list if no matches found.

    Example:
        >>> prompts = [prompt1, prompt2, prompt3]
        >>> results = search_prompts(prompts, "api")
        >>> all("api" in p.title.lower() or "api" in p.description.lower() for p in results)
        True
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.

    Validates that prompt content meets minimum requirements:
    - Not empty or None
    - Not just whitespace
    - At least 10 characters after stripping whitespace

    Args:
        content: The prompt content string to validate.

    Returns:
        True if content is valid, False otherwise.

    Example:
        >>> validate_prompt_content("Valid prompt content")
        True
        >>> validate_prompt_content("   ")
        False
        >>> validate_prompt_content("Too short")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Identifies and extracts all template variables from prompt text.
    Variables are expected in the format {{variable_name}} where variable_name
    contains only word characters (alphanumeric and underscore).

    Args:
        content: The prompt content string to extract variables from.

    Returns:
        List of variable names found in the content. Returns empty list if
        no variables found. Variable names are returned as they appear
        (without the {{ }} delimiters).

    Example:
        >>> extract_variables("Hello {{name}}, your age is {{age}}")
        ['name', 'age']
        >>> extract_variables("No variables here")
        []
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
