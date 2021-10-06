"""Schema module."""
import os
from typing import Any, Dict, List, Optional, Union

from datacatalogtordf.uri import InvalidURIError, URI
from modelldcatnotordf.modelldcatno import CodeElement, ModelElement
from skolemizer import Skolemizer

from jsonschematordf.component import Component
import jsonschematordf.componentfactory as component_factory
from jsonschematordf.types.enums import RECURSIVE_CHARACTER
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
        os.environ["skolemizer_baseurl"] = base_uri

    @property
    def base_uri(self) -> str:
        """Getter for base URI."""
        return self.__base_uri

    @property
    def orphan_elements(self) -> List[Union[ModelElement, CodeElement]]:
        """Getter for orphan elements."""
        return self.__orphans

    def get_components_by_path(self, path: str) -> List[Component]:
        """Attempt to get component by reference path."""
        path_list = path.split("/")
        return self.get_components_by_path_list(path_list)

    def get_components_by_path_list(self, path_list: List[str]) -> List[Component]:
        """Attempt to get component by reference path."""
        if len(path_list) > 0:
            non_relative_path = (
                path_list[1:] if path_list[0] == RECURSIVE_CHARACTER else path_list
            )
            component_title = path_list[-1]
            path_without_title = path_list[:-1]

            component_representation = nested_get(
                self.__json_schema_representation, *non_relative_path
            )
            if isinstance(component_representation, Dict):
                return component_factory.create_components(
                    path_without_title,
                    {"title": component_title, **component_representation},
                )
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

    def create_identifier(self, component_path: Optional[str]) -> URI:
        """Create identifier for component."""
        if component_path:
            try:
                component_uri = self.base_uri + component_path
                return URI(component_uri)
            except InvalidURIError:
                pass

        return Skolemizer.add_skolemization()
