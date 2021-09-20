"""Pytests."""
from modelldcatnotordf.modelldcatno import (
    Attribute,
    Choice,
    ObjectType,
    Role,
    SimpleType,
    Specialization,
)
from pytest_mock import MockerFixture
from rdflib.graph import Graph

import jsonschematordf.modelldcatnofactory as modelldcatno_factory
from jsonschematordf.types.constants import TYPE_DEFINITION_REFERENCE
from tests.testutils import assert_isomorphic


def test_create_model_property(mocker: MockerFixture) -> None:
    """Test that create_model_property returns correct property type. TODO."""
    mock_component = mocker.MagicMock()
    mock_schema = mocker.MagicMock()
    assert (
        modelldcatno_factory.create_model_property(mock_component, mock_schema) is None
    )


def test_create_model_element(mocker: MockerFixture) -> None:
    """Test that create_model_element returns correct element type. TODO."""
    mock_component = mocker.MagicMock()
    mock_schema = mocker.MagicMock()
    assert (
        modelldcatno_factory.create_model_element(mock_component, mock_schema) is None
    )


def test_create_valid_identifier(mocker: MockerFixture) -> None:
    """Test that valid attributes produces expeceted identifier."""
    title = "title"
    component_path = "components/schemas"
    base_uri = "http://uri.com"
    mock_component = mocker.MagicMock()
    mock_component.complete_path = f"{component_path}#{title}"

    mock_schema = mocker.MagicMock()
    mock_schema.base_uri = base_uri

    expected = f"{base_uri}/{component_path}#{title}"
    actual = modelldcatno_factory._create_identifier(mock_component, mock_schema)

    assert expected == actual


def test_create_invalid_identifier_returns_skolemized_identifier(
    mocker: MockerFixture,
) -> None:
    """Test that invalid attributes produces skolemized identifier."""
    title = "!!"
    component_path = "<path>"
    base_uri = "http://uri.com"
    mock_component = mocker.MagicMock()
    mock_component.path = f"#/{component_path}"
    mock_component.title = {None: title}

    mock_schema = mocker.MagicMock()
    mock_schema.base_uri = base_uri

    expected = "skolemized_id"
    skolemizer_mock = mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=expected,
    )
    actual = modelldcatno_factory._create_identifier(mock_component, mock_schema)

    assert expected == actual
    skolemizer_mock.assert_called_once


def test_no_title_returns_skolemized_identifier(mocker: MockerFixture) -> None:
    """Test that missing title produces skolemized identifier."""
    mock_component = mocker.MagicMock()
    mock_component.title = None

    mock_schema = mocker.MagicMock()

    expected = "skolemized_id"
    skolemizer_mock = mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=expected,
    )

    actual = modelldcatno_factory._create_identifier(mock_component, mock_schema)

    assert expected == actual
    skolemizer_mock.assert_called_once


def test_no_path_returns_skolemized_identifier(mocker: MockerFixture) -> None:
    """Test that missing path produces skolemized identifier."""
    mock_component = mocker.MagicMock()
    mock_component.path = None

    mock_schema = mocker.MagicMock()

    expected = "skolemized_id"
    skolemizer_mock = mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=expected,
    )

    actual = modelldcatno_factory._create_identifier(mock_component, mock_schema)

    assert expected == actual
    skolemizer_mock.assert_called_once


def test_no_base_uri_returns_skolemized_identifier(mocker: MockerFixture) -> None:
    """Test that missing base uri produces skolemized identifier."""
    mock_component = mocker.MagicMock()

    mock_schema = mocker.MagicMock()
    mock_schema.base_uri = None

    expected = "skolemized_id"
    skolemizer_mock = mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=expected,
    )

    actual = modelldcatno_factory._create_identifier(mock_component, mock_schema)

    assert expected == actual
    skolemizer_mock.assert_called_once


def test_creates_valid_object_type(mocker: MockerFixture) -> None:
    """Test that ObjectTypes are correctly created."""
    identifier = "identifier"
    title = {None: "title"}
    description = {None: "description"}
    child_identifier = "child_identifier"

    mock_component = mocker.MagicMock()
    mock_component.title = title
    mock_component.description = description
    mock_component.properties = [mocker.MagicMock()]

    mock_schema = mocker.MagicMock()

    add_parsed_component_mock = mocker.patch(
        "jsonschematordf.schema.Schema.add_parsed_component"
    )
    create_id_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )
    create_model_prop_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_property",
        return_value=child_identifier,
    )

    expected = ObjectType(identifier)
    expected.title = title
    expected.description = description
    expected.has_property = [child_identifier]

    actual = modelldcatno_factory._create_object_type(mock_component, mock_schema)

    assert isinstance(actual, ObjectType)
    add_parsed_component_mock.assert_called_once
    create_id_mock.assert_called_once
    create_model_prop_mock.assert_called_once
    assert actual.identifier == expected.identifier
    assert actual.title == expected.title
    assert actual.description == expected.description
    assert actual.has_property == expected.has_property

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_valid_simple_type(mocker: MockerFixture) -> None:
    """Test that SimpleTypes are correctly created."""
    identifier = "identifier"
    has_property_identifier = "has_property"
    title = {None: "title"}
    description = {None: "description"}
    type = "string"
    pattern = "pattern"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.type = type
    mock_component.pattern = pattern
    mock_component.min_length = 0
    mock_component.max_length = 10
    mock_component.format = None
    mock_component.minimum = None
    mock_component.maximum = None
    mock_component.exclusive_maximum = None
    mock_component.exclusive_minimum = None

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        side_effect=[identifier, has_property_identifier],
    )
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_specialization_property",
        return_value=has_property_identifier,
    )

    expected = SimpleType(identifier)
    expected.identifier = identifier
    expected.title = title
    expected.description = description
    expected.pattern = pattern
    expected.min_length = 0
    expected.max_length = 10
    expected.has_property = [has_property_identifier]

    actual = modelldcatno_factory._create_simple_type(mock_component, mock_schema)

    assert isinstance(actual, SimpleType)
    assert actual.identifier == expected.identifier
    assert actual.title == expected.title
    assert actual.description == expected.description
    assert actual.pattern == expected.pattern
    assert actual.min_length == expected.min_length
    assert actual.max_length == expected.max_length
    assert actual.has_property[0] == has_property_identifier

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_simple_type_exclusive_values_set_correctly(mocker: MockerFixture) -> None:
    """Test that exclusive min and max is set correctly."""
    identifier = "identifier"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.minimum = 0
    mock_component.maximum = 10
    mock_component.exclusive_maximum = True
    mock_component.exclusive_maximum = True
    mock_component.title = None
    mock_component.description = None
    mock_component.pattern = None
    mock_component.min_length = None
    mock_component.max_length = None

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )

    expected = SimpleType(identifier)
    expected.min_exclusive = 0
    expected.max_exclusive = 10

    actual = modelldcatno_factory._create_simple_type(mock_component, mock_schema)

    assert actual.min_exclusive == expected.min_exclusive
    assert actual.max_exclusive == expected.max_exclusive

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_simple_type_inclusive_values_set_correctly(mocker: MockerFixture) -> None:
    """Test that inclusive min and max is set correctly."""
    identifier = "identifier"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.minimum = 0
    mock_component.maximum = 10
    mock_component.exclusive_minimum = False
    mock_component.exclusive_maximum = False
    mock_component.title = None
    mock_component.description = None
    mock_component.pattern = None
    mock_component.min_length = None
    mock_component.max_length = None

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )

    expected = SimpleType(identifier)
    expected.min_inclusive = 0
    expected.max_inclusive = 10

    actual = modelldcatno_factory._create_simple_type(mock_component, mock_schema)

    assert actual.min_inclusive == expected.min_inclusive
    assert actual.max_inclusive == expected.max_inclusive

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_valid_primitive_simple_type(mocker: MockerFixture) -> None:
    """Test that primitve SimpleTypes are correctly created."""
    identifier = "identifier"
    type = "string"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.type = type
    mock_component.format = None

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )

    expected = SimpleType(identifier)
    expected.identifier = identifier
    expected.title = {None: type}
    expected.type_definition_reference = TYPE_DEFINITION_REFERENCE.get(type)

    actual = modelldcatno_factory._create_primitive_simple_type(
        mock_component, mock_schema
    )

    assert isinstance(actual, SimpleType)
    assert actual.identifier == expected.identifier
    assert actual.title == expected.title
    assert actual.type_definition_reference == expected.type_definition_reference

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_specialization_property(mocker: MockerFixture) -> None:
    """Tests creation of Specialization model property."""
    specialiation_identifier = "specialiation_identifier"
    simple_type_identifier = "simple_type_identifier"
    type = "string"

    mock_component = mocker.MagicMock()
    mock_component.identifier = specialiation_identifier
    mock_component.type = type
    mock_component.format = None

    mock_schema = mocker.MagicMock()

    primitive_simple_type = SimpleType(simple_type_identifier)
    primitive_simple_type.title = {None: type}
    primitive_simple_type.type_definition_reference = TYPE_DEFINITION_REFERENCE.get(
        type
    )

    expected = Specialization(specialiation_identifier)
    expected.has_general_concept = primitive_simple_type

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        side_effect=[specialiation_identifier, simple_type_identifier],
    )

    actual = modelldcatno_factory._create_specialization_property(
        mock_component, mock_schema
    )
    actual_general_concept = actual.has_general_concept

    assert actual_general_concept.title == primitive_simple_type.title
    assert (
        actual_general_concept.type_definition_reference
        == primitive_simple_type.type_definition_reference
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_attribute_model_property(mocker: MockerFixture) -> None:
    """Test that attribute properties are correctly created."""
    attribute_identifier = "identifier"
    type = "string"
    title = {None: "title"}
    description = {None: "description"}
    max_occurs = "1"
    min_occurs = "1"

    mock_component = mocker.MagicMock()
    mock_component.identifier = attribute_identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.type = type
    mock_component.format = None
    mock_component.min_occurs = min_occurs
    mock_component.max_occurs = max_occurs

    mock_schema = mocker.MagicMock()

    simple_type_identifier = "simple_identifier"
    simple_type = SimpleType(simple_type_identifier)
    simple_type.title = {None: type}
    simple_type.type_definition_reference = TYPE_DEFINITION_REFERENCE.get(type)

    expected = Attribute(attribute_identifier)
    expected.title = title
    expected.description = description
    expected.max_occurs = max_occurs
    expected.min_occurs = min_occurs
    expected.has_simple_type = simple_type

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        side_effect=[attribute_identifier, simple_type_identifier],
    )

    actual = modelldcatno_factory._create_attribute_property(
        mock_component, mock_schema
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_choice_property(mocker: MockerFixture) -> None:
    """Test that choice properties are correctly created."""
    identifier = "identifier"
    title = {None: "title"}
    description = {None: "description"}
    min_occurs = "1"
    max_occurs = "2"
    one_of_uri = "one_of"
    one_of = [one_of_uri]

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.min_occurs = min_occurs
    mock_component.max_occurs = max_occurs
    mock_component.one_of = one_of

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )
    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        return_value=one_of_uri,
    )

    expected = Choice(identifier)
    expected.title = title
    expected.description = description
    expected.has_some = [one_of_uri]
    expected.min_occurs = min_occurs
    expected.max_occurs = max_occurs

    actual = modelldcatno_factory._create_choice_property(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_object_array_property(mocker: MockerFixture) -> None:
    """Test that object array properties are correctly created."""
    identifier = "identifier"
    title = {None: "title"}
    description = {None: "description"}
    min_occurs = "1"
    max_occurs = "2"
    item_identifier = "item_identifier"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.min_occurs = min_occurs
    mock_component.max_occurs = max_occurs
    mock_component.items = mocker.MagicMock()

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )
    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        return_value=item_identifier,
    )

    expected = Role(identifier)
    expected.title = title
    expected.description = description
    expected.min_occurs = min_occurs
    expected.max_occurs = max_occurs
    expected.has_object_type = item_identifier

    actual = modelldcatno_factory._create_object_array_property(
        mock_component, mock_schema
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


def test_creates_simple_type_array_property(mocker: MockerFixture) -> None:
    """Test that simple type array properties are correctly created."""
    identifier = "identifier"
    title = {None: "title"}
    description = {None: "description"}
    min_occurs = "1"
    max_occurs = "2"
    item_identifier = "item_identifier"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.min_occurs = min_occurs
    mock_component.max_occurs = max_occurs

    mock_schema = mocker.MagicMock()

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )
    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        return_value=item_identifier,
    )

    expected = Attribute(identifier)
    expected.title = title
    expected.description = description
    expected.min_occurs = min_occurs
    expected.max_occurs = max_occurs
    expected.has_simple_type = item_identifier

    actual = modelldcatno_factory._create_simple_type_array_property(
        mock_component, mock_schema
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)
