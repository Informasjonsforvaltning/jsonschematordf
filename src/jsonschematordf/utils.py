"""Utility functions module."""
from typing import Any, Dict, Optional

from datacatalogtordf.uri import InvalidURIError, URI

from jsonschematordf.types.enums import (
    EMPTY_PATH,
    EXTERNAL_REFERENCE,
    RECURSIVE_REFERENCE,
)


def nested_get(dictionary: Dict, *keys: str) -> Optional[Any]:
    """Get nested object from dict."""
    if len(keys) > 1:
        return nested_get(dictionary.get(keys[0], {}), *keys[1:])
    elif len(keys) == 1:
        return dictionary.get(keys[0])
    else:
        raise TypeError("nested_get expected at least 1 key, got 0")


def determine_reference_type(reference: Optional[str]) -> Optional[str]:
    """Determine whether refernce string is recursive, external, or invalid."""
    if reference:
        if reference.startswith(EMPTY_PATH):
            return RECURSIVE_REFERENCE
        if reference.startswith("http"):
            try:
                URI(reference)
                return EXTERNAL_REFERENCE
            except InvalidURIError:
                return None
    return None
