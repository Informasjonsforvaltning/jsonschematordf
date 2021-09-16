"""Utility functions module."""
from typing import Any, Dict, Optional


def nested_get(dictionary: Dict, *keys: str) -> Optional[Any]:
    """Get nested object from dict."""
    if len(keys) > 1:
        return nested_get(dictionary.get(keys[0], {}), *keys[1:])
    elif len(keys) == 1:
        return dictionary.get(keys[0])
    else:
        raise TypeError("nested_get expected at least 1 key, got 0")
