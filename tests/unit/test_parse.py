"""Pytests."""
from typing import Dict, List

import pytest
from pytest_mock.plugin import MockerFixture

from jsonschematordf.parse import (
    json_schema_component_to_modelldcatno,
    json_schema_to_graph,
    json_schema_to_modelldcatno,
)
from jsonschematordf.parsedschema import ParsedSchema
from jsonschematordf.schema import Schema


@pytest.mark.unit
def test_json_schema_to_graph(mocker: MockerFixture) -> None:
    """Test that components are parsed and added to graph."""
    json_schema_string = "{ 'Element': { 'type': 'object' } }"
    base_uri = "http://uri.com"

    graph_mock_output = mocker.MagicMock()

    parse_mock = mocker.patch(
        "jsonschematordf.parse.json_schema_to_modelldcatno",
        return_value=([mocker.MagicMock()], [mocker.MagicMock()]),
    )
    graph_mock = mocker.patch(
        "jsonschematordf.parse.add_elements_to_graph", return_value=graph_mock_output
    )

    actual = json_schema_to_graph(json_schema_string, base_uri)

    assert actual == graph_mock_output
    parse_mock.assert_called_once()
    graph_mock.assert_called_once()


@pytest.mark.unit
def test_json_schema_to_modelldcatno(mocker: MockerFixture) -> None:
    """Test that components are parsed."""
    json_schema_string = "{ 'Element': { 'type': 'object' } }"
    base_uri = "http://uri.com"

    mock_element = [mocker.MagicMock()]
    mock_orphan = [mocker.MagicMock()]

    parsed_schema_mock = mocker.MagicMock()
    parsed_schema_mock.model_elements = mock_element
    parsed_schema_mock.orphan_elements = mock_orphan

    parse_mock = mocker.patch(
        "jsonschematordf.parse.json_schema_component_to_modelldcatno",
        return_value=parsed_schema_mock,
    )

    model_elements, orphan_elements = json_schema_to_modelldcatno(
        json_schema_string, base_uri
    )

    assert model_elements == mock_element
    assert orphan_elements == mock_orphan
    parse_mock.assert_called_once()


@pytest.mark.unit
def test_json_schema_to_modelldcatno_returns_empty() -> None:
    """Test that empty ParsedSchema is returned if invalid JSON Schema is passed."""
    json_schema_string = ""
    base_uri = "http://uri.com"

    parsed_schema = json_schema_to_modelldcatno(json_schema_string, base_uri)

    assert ParsedSchema() == parsed_schema


@pytest.mark.unit
def test_json_schema_component_to_modelldcatno(mocker: MockerFixture) -> None:
    """Test that components are parsed and added to graph."""
    json_schema_dict = {"schemas": {"Element": {"type": "object"}}}
    base_uri = "http://uri.com"
    schema = Schema(base_uri, json_schema_dict)
    path = ["schemas", "Element"]

    mock_element = mocker.MagicMock()

    get_component_mock = mocker.patch(
        "jsonschematordf.schema.Schema.get_components_by_path_list",
        return_value=[mocker.MagicMock()],
    )
    create_model_element_mock = mocker.patch(
        "jsonschematordf.parse.create_model_element", return_value=mock_element
    )
    mocker.patch(
        "jsonschematordf.schema.Schema.orphan_elements",
        return_value=mocker.MagicMock(),
    )

    model_elements, orphan_elements = json_schema_component_to_modelldcatno(
        schema, path
    )
    assert model_elements == [mock_element]
    assert isinstance(orphan_elements, mocker.MagicMock)
    get_component_mock.assert_called_once()
    create_model_element_mock.assert_called_once()


@pytest.mark.unit
def test_json_schema_component_to_modelldcatno_returns_empty() -> None:
    """Test that empty ParsedSchema is returned if invalid JSON Schema is passed."""
    json_schema_dict: Dict[str, str] = {}
    base_uri = "http://uri.com"
    schema = Schema(base_uri, json_schema_dict)
    path: List[str] = []

    parsed_schema = json_schema_component_to_modelldcatno(schema, path)

    assert ParsedSchema() == parsed_schema
