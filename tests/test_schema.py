"""Pytests."""
from datacatalogtordf.exceptions import InvalidURIError
from datacatalogtordf.uri import URI
import pytest
from pytest_mock import MockerFixture

from jsonschematordf.component import Component
from jsonschematordf.schema import Schema
from jsonschematordf.types.exceptions import ComponentAlreadyExistsException


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

    json_schema = {
        "path": {
            "to": {"component": {"title": component_title, "type": component_type}}
        }
    }

    schema = Schema(base_uri, json_schema)

    components = schema.get_components_by_path("#/path/to/component")

    assert len(components) == 1

    component = components[0]
    assert isinstance(component, Component)
    assert component.title == {None: component_title}
    assert component.type == component_type[0]


def test_recursive_path_returns_uri() -> None:
    """Test that recursive paths can return correct URIs."""
    base_uri = "https://uri.com"
    component_uri = "https://test.com#Test"

    json_schema = {"path": {"to": {"component": component_uri}}}

    schema = Schema(base_uri, json_schema)

    components = schema.get_components_by_path("#/path/to/component")

    assert len(components) == 1

    component = components[0]
    assert isinstance(component, URI)
    assert component == component_uri


def test_external_path_returns_uri() -> None:
    """Test that external path returns URI."""
    base_uri = "https://uri.com"
    path = "https://test.com#Test"

    schema = Schema(base_uri, {})

    components = schema.get_components_by_path(path)

    assert len(components) == 1

    component = components[0]

    assert component == path


def test_invalid_path__returns_empty_list() -> None:
    """Test that invalid path returns no components or URIs."""
    base_uri = "https://uri.com"
    path = "<test>"

    schema = Schema(base_uri, {})

    components = schema.get_components_by_path(path)

    assert len(components) == 0

    assert components == []


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


def test_parsed_component_collision_throws_exceptions(mocker: MockerFixture) -> None:
    """Test that collisions in parsed component cache throws exception."""
    with pytest.raises(ComponentAlreadyExistsException):
        base_uri = "https://uri.com"
        complete_path = "/path/to/component#Test"
        identifier = f"{base_uri}{complete_path}"

        mock_component = mocker.MagicMock()
        mock_component.complete_path = complete_path
        mock_component.identifier = identifier

        schema = Schema(base_uri, {})

        schema.add_parsed_component(mock_component)
        schema.add_parsed_component(mock_component)


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
