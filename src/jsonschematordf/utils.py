"""Utility functions module."""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from datacatalogtordf.uri import InvalidURIError, URI
from modelldcatnotordf.modelldcatno import CodeElement, ModelElement
from rdflib.graph import Graph

from jsonschematordf.types.enums import (
    EXTERNAL_REFERENCE,
    RECURSIVE_CHARACTER,
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
        if reference.startswith(RECURSIVE_CHARACTER):
            return RECURSIVE_REFERENCE
        if reference.startswith("http"):
            try:
                URI(reference)
                return EXTERNAL_REFERENCE
            except InvalidURIError:
                return None
    return None


def add_to_path(path: List[str], to_add: Optional[str]) -> List[str]:
    """Adds postfix to path list if exists, else returns empty path."""
    if to_add:
        return [*path, to_add]
    else:
        return [RECURSIVE_CHARACTER]


def add_elements_to_graph(
    graph: Graph, elements: List[Union[ModelElement, CodeElement]]
) -> Graph:
    """Get Graph containing all elements."""
    out_graph = deepcopy(graph)
    for element in elements:
        if isinstance(element, ModelElement) or isinstance(element, CodeElement):
            out_graph.parse(data=element.to_rdf(format="turtle"), format="turtle")

    return out_graph
