"""Schema module."""
from typing import Any, Dict, List, Optional, Union

from datacatalogtordf.exceptions import InvalidURIError
from datacatalogtordf.uri import URI

from jsonschematordf.component import Component
import jsonschematordf.componentfactory as component_factory
from jsonschematordf.types.enums import EMPTY_PATH
from jsonschematordf.types.exceptions import ComponentAlreadyExistsException
from jsonschematordf.utils import nested_get


class Schema:
    """Utility class for managing schema components."""

    __base_uri: URI
    __json_schema_representation: Dict[str, Any]
    __parsed_components_cache: Dict[str, URI]

    def __init__(
        self, base_uri: URI, json_schema_representation: Dict[str, Any]
    ) -> None:
        """Constructor for Schema object."""
        self.__base_uri = URI(base_uri)
        self.__json_schema_representation = json_schema_representation
        self.__parsed_components_cache = {}

    @property
    def base_uri(self) -> str:
        """Getter for base URI."""
        return self.__base_uri

    def _get_schema_component_at_path(self, path: str) -> List[Union[Component, URI]]:
        """Attempt to get component by reference path."""
        component_representation = nested_get(
            self.__json_schema_representation, *path.split("/")[1:]
        )
        if isinstance(component_representation, Dict):
            return component_factory.create_components(path, component_representation)
        elif isinstance(component_representation, str):
            return [URI(component_representation)]
        return []

    def get_components_by_path(self, path: str) -> List[Union[Component, URI]]:
        """Resolve internal or external resource."""
        try:
            if path[0] == EMPTY_PATH:
                return self._get_schema_component_at_path(path)
            return [URI(path)]
        except InvalidURIError:
            pass
        return []

    def add_parsed_component(
        self, complete_path: str, component_identifier: URI
    ) -> None:
        """Add a modelldcatno component or URI to parsed components cache."""
        if self.__parsed_components_cache.get(complete_path) is None:
            self.__parsed_components_cache[complete_path] = URI(component_identifier)
        else:
            raise ComponentAlreadyExistsException(
                f"Component at {complete_path} already exists."
            )

    def get_parsed_component(self, path: str) -> Optional[URI]:
        """Get a modelldcatno component or URI from parsed components cache."""
        return self.__parsed_components_cache.get(path)
