"""pytests."""

import pytest

from jsonschematordf.types.enums import (
    EXTERNAL_REFERENCE,
    RECURSIVE_REFERENCE,
)
from jsonschematordf.utils import determine_reference_type, nested_get


@pytest.mark.unit
def test_nested_get_retrieves_correct_entry() -> None:
    """Nested get should return correct entry."""
    expected = "d"
    dictionary = {"a": {"b": {"c": expected}}}
    assert nested_get(dictionary, "a", "b", "c") == expected


@pytest.mark.unit
def test_nested_get_returns_none_for_non_existing_key() -> None:
    """Nested get should return none for missing key."""
    dictionary = {"a": {"b": {"c": "d"}}}
    assert nested_get(dictionary, "c", "b", "a") is None


@pytest.mark.unit
def test_nested_get_throws_for_no_keys() -> None:
    """Nested get should throw type error for call without one or more keys."""
    with pytest.raises(TypeError):
        dictionary = {"a": {"b": {"c": "d"}}}
        nested_get(dictionary)


@pytest.mark.unit
def test_determine_reference_type_recursive() -> None:
    """Should return recursive reference type."""
    reference = "#/test"
    assert determine_reference_type(reference) == RECURSIVE_REFERENCE


@pytest.mark.unit
def test_determine_reference_type_external() -> None:
    """Should return external reference type."""
    reference = "http://uri.com#test"
    assert determine_reference_type(reference) == EXTERNAL_REFERENCE


@pytest.mark.unit
def test_determine_reference_type_none() -> None:
    """Should return None."""
    reference = "test"
    assert determine_reference_type(reference) is None
    assert determine_reference_type(None) is None


@pytest.mark.unit
def test_invalid_uri_should_return_none() -> None:
    """Invalid URI should raise exception."""
    reference = "http://uri<.com"
    determine_reference_type(reference)
