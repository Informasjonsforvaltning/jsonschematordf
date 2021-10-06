"""JsonSchemaToRDF module."""
from typing import List

from rdflib.graph import Graph
import yaml

from jsonschematordf.modelldcatnofactory import create_model_element
from jsonschematordf.parsedschema import ParsedSchema
from jsonschematordf.schema import Schema
from jsonschematordf.utils import add_elements_to_graph


def json_schema_to_graph(json_schema_string: str, base_uri: str) -> Graph:
    """Parse JSON Schema to RDF Graph representation.

    Args:
        json_schema_string: a valid JSON Schema string.
        base_uri: base URI of the schema.

    Returns:
        an RDF Graph representing the JSON Schema using modelldcatno.

    Example:
    >>> from jsonschematordf.parse import json_schema_to_graph
    >>> json_schema_string = "{ 'Element': { 'type': 'object' } }"
    >>> base_uri = "http://uri.com"
    >>> graph = json_schema_to_graph(json_schema_string, base_uri)
    """
    model_elements, orphan_elements = json_schema_to_modelldcatno(
        json_schema_string, base_uri
    )

    schema_graph = add_elements_to_graph(Graph(), [*model_elements, *orphan_elements])

    return schema_graph


def json_schema_to_modelldcatno(json_schema_string: str, base_uri: str) -> ParsedSchema:
    """Parse JSON Schema to modelldcatno representation.

    Args:
        json_schema_string: A valid JSON Schema string.
        base_uri: Base URI of the schema.

    Returns:
        A ParsedSchema object containing the parsed modelldcatno ModelElements and
        orphaned elements.

    Example:
    >>> from jsonschematordf.parse import json_schema_to_modelldcatno
    >>> json_schema_string = "{ 'Element': { 'type': 'object' } }"
    >>> base_uri = "http://uri.com"
    >>> model_elements, orphan_elements = json_schema_to_modelldcatno(
        ... json_schema_string, base_uri
        ...)
    """
    in_dict = yaml.safe_load(json_schema_string)
    model_elements = []
    orphan_elements = []

    if isinstance(in_dict, dict):
        schema = Schema(base_uri, in_dict)
        for root_element in in_dict.keys():
            parsed_schema = json_schema_component_to_modelldcatno(
                schema, [root_element]
            )
            model_elements.extend(parsed_schema.model_elements)
            orphan_elements.extend(parsed_schema.orphan_elements)
        return ParsedSchema(model_elements, orphan_elements)

    return ParsedSchema()


def json_schema_component_to_modelldcatno(
    schema: Schema, path: List[str]
) -> ParsedSchema:
    """Parse a single component in a JSON Schema to a modelldcatno representation.

    Args:
        schema: A jsonschematordf Schema object.
        path: Path to the component to be serialized.

    Returns:
        A ParsedSchema object containing the parsed modelldcatno ModelElements and
        orphaned elements.


    Example:
    >>> from jsonschematordf.parse import json_schema_component_to_modelldcatno
    >>> from jsonschematordf.schema import Schema
    >>> json_schema_string = "{ 'schemas': { 'Element': { 'type': 'object' } } }"
    >>> base_uri = "http://uri.com"
    >>> schema = Schema(base_uri, json_schema_string)
    >>> path = ["schemas", "Element"]
    >>> model_elements, orphan_elements = json_schema_component_to_modelldcatno(
        ... schema, path
        ...)
    """
    model_elements = []
    components = schema.get_components_by_path_list(path)

    for component in components:
        parsed_element = create_model_element(component, schema)
        if parsed_element:
            model_elements.append(parsed_element)

    return ParsedSchema(model_elements, schema.orphan_elements)
