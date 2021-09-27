"""Pytests."""
from datacatalogtordf.exceptions import InvalidURIError
from modelldcatnotordf.modelldcatno import CodeElement, ObjectType
import pytest
from pytest_mock import MockerFixture
from rdflib import Graph


from jsonschematordf.component import Component
from jsonschematordf.schema import Schema
from tests.testutils import assert_isomorphic


def test_creates_valid_schema() -> None:
    """Test that valid schema is created."""
    base_uri = "https://uri.com"

    schema = Schema(base_uri, {})

    assert schema.base_uri == base_uri


def test_does_not_create_invalid_schema() -> None:
    """Test that invalid schema base URI raises InvalidURIError."""
    with pytest.raises(InvalidURIError):
        base_uri = "<>"
        Schema(base_uri, {})


def test_recursive_path_returns_component() -> None:
    """Test that recursive paths returns correct components."""
    base_uri = "https://uri.com"
    component_title = "title"
    component_type = ["string"]

    json_schema = {"path": {"to": {component_title: {"type": component_type}}}}

    schema = Schema(base_uri, json_schema)

    components = schema.get_components_by_path(f"#/path/to/{component_title}")

    assert len(components) == 1

    component = components[0]
    assert isinstance(component, Component)
    assert component.title == {None: component_title}
    assert component.type == component_type[0]


def test_unused_path__returns_empty_list() -> None:
    """Test that invalid path returns no components or URIs."""
    base_uri = "https://uri.com"
    path = "#/test"

    schema = Schema(base_uri, {})

    components = schema.get_components_by_path(path)

    assert len(components) == 0

    assert components == []


def test_parsed_components_get_and_set(mocker: MockerFixture) -> None:
    """Test getting and setting of parsed components."""
    base_uri = "https://uri.com"
    complete_path = "/path/to/component#Test"
    identifier = f"{base_uri}{complete_path}"

    mock_component = mocker.MagicMock()
    mock_component.complete_path = complete_path
    mock_component.identifier = identifier

    schema = Schema(base_uri, {})

    schema.add_parsed_component(mock_component)

    component_uri = schema.get_parsed_component_uri(complete_path)

    assert component_uri == identifier


def test_set_parsed_component_with_invalid_uri_throws_exception(
    mocker: MockerFixture,
) -> None:
    """Test set parsed component with invalid uri raises InvalidURIError."""
    with pytest.raises(InvalidURIError):
        base_uri = "https://uri.com"
        complete_path = "/path/to/component#Test"
        identifier = "<><>"

        mock_component = mocker.MagicMock()
        mock_component.complete_path = complete_path
        mock_component.identifier = identifier

        schema = Schema(base_uri, {})

        schema.add_parsed_component(mock_component)


def test_orphan_element_graph_creation() -> None:
    """Test that orphan elements are added and that the returned graph is correct."""
    base_uri = "https://uri.com"
    code_element_uri = f"{base_uri}#CodeElement"
    object_type_uri = f"{base_uri}#ObjectType"

    code_element = CodeElement(code_element_uri)
    object_type = ObjectType(object_type_uri)

    schema = Schema(base_uri, {})

    schema.add_orphan_elements([code_element, object_type])

    expected = """
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    <https://uri.com#CodeElement> a modelldcatno:CodeElement .
    <https://uri.com#ObjectType> a modelldcatno:ObjectType .
    """

    actual = schema.get_orphan_elements_graph()

    expected = Graph().parse(data=expected, format="turtle")

    assert_isomorphic(expected, actual)
