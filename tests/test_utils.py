"""pytests."""

import pytest

from jsonschematordf.utils import nested_get


def test_nested_get_retrieves_correct_entry() -> None:
    """Nested get should return correct entry."""
    expected = "d"
    dictionary = {"a": {"b": {"c": expected}}}
    assert nested_get(dictionary, "a", "b", "c") == expected


def test_nested_get_returns_none_for_non_existing_key() -> None:
    """Nested get should return none for missing key."""
    dictionary = {"a": {"b": {"c": "d"}}}
    assert nested_get(dictionary, "c", "b", "a") is None


def test_nested_get_throws_for_no_keys() -> None:
    """Nested get should throw type error for call without one or more keys."""
    with pytest.raises(TypeError):
        dictionary = {"a": {"b": {"c": "d"}}}
        nested_get(dictionary)
