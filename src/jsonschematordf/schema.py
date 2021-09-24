"""Schema module."""
from typing import Any, Dict, List, Optional, Union

from datacatalogtordf.uri import URI
from modelldcatnotordf.modelldcatno import CodeElement, ModelElement
from rdflib import Graph

from jsonschematordf.component import Component
import jsonschematordf.componentfactory as component_factory
from jsonschematordf.utils import nested_get


class Schema:
    """Utility class for managing schema components."""

    __slots__ = (
        "__base_uri",
        "__json_schema_representation",
        "__parsed_components_cache",
        "__orphans",
    )

    __base_uri: URI
    __json_schema_representation: Dict[str, Any]
    __parsed_components_cache: Dict[str, URI]
    __orphans: List[Union[ModelElement, CodeElement]]

    def __init__(
        self, base_uri: URI, json_schema_representation: Dict[str, Any]
    ) -> None:
        """Constructor for Schema object."""
        self.__base_uri = URI(base_uri)
        self.__json_schema_representation = json_schema_representation
        self.__parsed_components_cache = {}
        self.__orphans = []

    @property
    def base_uri(self) -> str:
        """Getter for base URI."""
        return self.__base_uri

    def get_components_by_path(self, path: str) -> List[Component]:
        """Attempt to get component by reference path."""
        path_list = path.split("/")
        component_representation = nested_get(
            self.__json_schema_representation, *path_list[1:]
        )
        component_title = path_list[-1]
        if isinstance(component_representation, Dict):
            return component_factory.create_components(
                path, {"title": component_title, **component_representation}
            )
        else:
            return []

    def add_parsed_component(self, component: Component) -> None:
        """Add a modelldcatno component or URI to parsed components cache."""
        if component.complete_path:
            self.__parsed_components_cache[component.complete_path] = URI(
                component.identifier
            )

    def get_parsed_component_uri(self, path: Optional[str]) -> Optional[URI]:
        """Get a modelldcatno component or URI from parsed components cache."""
        return self.__parsed_components_cache.get(path) if path else None

    def add_orphan_elements(
        self, orphans: List[Union[ModelElement, CodeElement]]
    ) -> None:
        """Add orphan elements to be included in final graph."""
        self.__orphans.extend(orphans)

    def get_orphan_elements_graph(self) -> Graph:
        """Get Graph containing all orphan elements."""
        out_graph = Graph()
        for orphan_element in self.__orphans:
            out_graph.parse(data=orphan_element.to_rdf(), format="turtle")

        return out_graph
