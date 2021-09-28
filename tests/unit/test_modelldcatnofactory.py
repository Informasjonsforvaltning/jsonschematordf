"""Pytests."""
from datacatalogtordf.uri import URI
from modelldcatnotordf.modelldcatno import (
    Attribute,
    Choice,
    CodeElement,
    CodeList,
    ModelElement,
    ObjectType,
    Role,
    SimpleType,
    Specialization,
)
import pytest
from pytest_mock import MockerFixture
from rdflib.graph import Graph

from jsonschematordf.component import Component
import jsonschematordf.modelldcatnofactory as modelldcatno_factory
from jsonschematordf.types.constants import TYPE_DEFINITION_REFERENCE
from jsonschematordf.types.enums import EXTERNAL_REFERENCE, RECURSIVE_REFERENCE
from tests.testutils import assert_isomorphic


@pytest.mark.unit
def test_create_model_property(mocker: MockerFixture) -> None:
    """Test that create_model_property returns correct property type."""
    mock_component = mocker.MagicMock()
    mock_component.description = None
    mock_component.enum = None
    mock_component.exclusive_maximum = None
    mock_component.exclusive_minimum = None
    mock_component.format = None
    mock_component.items = None
    mock_component.max_length = None
    mock_component.maximum = None
    mock_component.min_length = None
    mock_component.minimum = None
    mock_component.one_of = None
    mock_component.pattern = None
    mock_component.specializes = None
    mock_component.title = None
    mock_component.type = None
    mock_component.properties = None

    mock_schema = mocker.MagicMock()
    mocker.patch.object(mock_schema, "get_parsed_component_uri", return_value=None)

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch("jsonschematordf.modelldcatnofactory._create_identifier",)

    role_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_role_property",
    )
    attribute_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_attribute_property",
    )
    choice_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_choice_property",
    )
    specialization_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_specialization_property",
    )
    object_array_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_object_array_property",
    )
    simple_type_array_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_simple_type_array_property",
    )

    mock_component.type = "object"
    modelldcatno_factory.create_model_property(mock_component, mock_schema)
    role_creator_mock.assert_called_once()
    mock_component.type = None

    mock_component.type = "string"
    modelldcatno_factory.create_model_property(mock_component, mock_schema)
    attribute_creator_mock.assert_called_once()
    mock_component.type = None

    mock_component.one_of = [mocker.MagicMock()]
    modelldcatno_factory.create_model_property(mock_component, mock_schema)
    choice_creator_mock.assert_called_once()
    mock_component.one_of = None

    mock_component.specializes = mocker.MagicMock()
    modelldcatno_factory.create_model_property(mock_component, mock_schema)
    specialization_creator_mock.assert_called_once()
    mock_component.specializes = None

    items_mock = mocker.MagicMock()
    items_mock.type = "object"
    items_mock.items = None
    items_mock.specializes = None
    items_mock.one_of = None
    items_mock.enum = None
    items_mock.properties = None
    mock_component.items = items_mock
    modelldcatno_factory.create_model_property(mock_component, mock_schema)
    object_array_creator_mock.assert_called_once()
    mock_component.items = None

    items_mock.type = "string"
    mock_component.items = items_mock
    modelldcatno_factory.create_model_property(mock_component, mock_schema)
    simple_type_array_creator_mock.assert_called_once()
    mock_component.items = None


@pytest.mark.unit
def test_create_model_element(mocker: MockerFixture) -> None:
    """Test that create_model_element returns correct element type."""
    mock_component = mocker.MagicMock()
    mock_component.description = None
    mock_component.enum = None
    mock_component.exclusive_maximum = None
    mock_component.exclusive_minimum = None
    mock_component.format = None
    mock_component.items = None
    mock_component.max_length = None
    mock_component.maximum = None
    mock_component.min_length = None
    mock_component.minimum = None
    mock_component.one_of = None
    mock_component.pattern = None
    mock_component.specializes = None
    mock_component.title = None
    mock_component.type = None
    mock_component.ref = None
    mock_component.properties = None

    mock_schema = mocker.MagicMock()
    mocker.patch.object(mock_schema, "get_parsed_component_uri", return_value=None)

    mocker.patch("jsonschematordf.schema.Schema.add_parsed_component")
    mocker.patch("jsonschematordf.modelldcatnofactory._create_identifier",)

    object_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_object_type",
    )
    simple_type_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_simple_type",
    )
    primitive_simple_type_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_primitive_simple_type",
    )
    code_list_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_code_list",
    )

    mock_component.type = "object"
    modelldcatno_factory.create_model_element(mock_component, mock_schema)
    object_creator_mock.assert_called_once()
    mock_component.type = None

    mock_component.type = "string"
    mock_component.title = {None: "title"}
    modelldcatno_factory.create_model_element(mock_component, mock_schema)
    simple_type_creator_mock.assert_called_once()
    mock_component.type = None
    mock_component.title = None

    mock_component.type = "string"
    mock_component.format = "datetime"
    modelldcatno_factory.create_model_element(mock_component, mock_schema)
    primitive_simple_type_creator_mock.assert_called_once()
    mock_component.type = None
    mock_component.format = None

    mock_component.enum = ["test"]
    modelldcatno_factory.create_model_element(mock_component, mock_schema)
    code_list_creator_mock.assert_called_once()
    mock_component.enum = None


@pytest.mark.unit
def test_create_model_element_resolves_ref(mocker: MockerFixture) -> None:
    """Create model element should resolve referenced component."""
    ref_identifier = "identifier"

    mock_component = mocker.MagicMock()

    mock_schema = mocker.MagicMock()
    mocker.patch.object(mock_schema, "get_parsed_component_uri", return_value=None)

    mocker.patch(
        "jsonschematordf.modelldcatnofactory._resolve_component_reference",
        return_value=ref_identifier,
    )

    assert (
        modelldcatno_factory.create_model_element(mock_component, mock_schema)
        == ref_identifier
    )


@pytest.mark.unit
def test_resolve_component_reference_resolves_recursive_reference(
    mocker: MockerFixture,
) -> None:
    """Returns result of recursive reference resolution."""
    mock_reference = mocker.MagicMock()
    mock_schema = mocker.MagicMock()
    expected = "identifier"

    mocker.patch(
        "jsonschematordf.modelldcatnofactory._resolve_recursive_reference",
        return_value=expected,
    )
    mocker.patch(
        "jsonschematordf.modelldcatnofactory.determine_reference_type",
        return_value=RECURSIVE_REFERENCE,
    )
    assert (
        modelldcatno_factory._resolve_component_reference(mock_reference, mock_schema)
        == expected
    )


@pytest.mark.unit
def test_resolve_component_reference_resolves_external_reference(
    mocker: MockerFixture,
) -> None:
    """Returns URI of external reference."""
    mock_reference = mocker.MagicMock()
    mock_schema = mocker.MagicMock()

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.determine_reference_type",
        return_value=EXTERNAL_REFERENCE,
    )
    assert (
        modelldcatno_factory._resolve_component_reference(mock_reference, mock_schema)
        == mock_reference
    )


@pytest.mark.unit
def test_resolve_component_reference_returns_none(mocker: MockerFixture) -> None:
    """Returns None if reference cannot be resolved."""
    mock_reference = mocker.MagicMock()
    mock_schema = mocker.MagicMock()

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.determine_reference_type",
        return_value="None",
    )
    assert (
        modelldcatno_factory._resolve_component_reference(mock_reference, mock_schema)
        is None
    )


@pytest.mark.unit
def test_resolve_recursive_reference_returns_and_adds_orphan(
    mocker: MockerFixture,
) -> None:
    """Returns first referenced component and adds orphans to schema."""
    component = mocker.MagicMock(spec=ModelElement)
    orphan = mocker.MagicMock(spec=ModelElement)
    model_element_uris = [None, component, None, orphan]

    object_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        side_effect=model_element_uris,
    )

    mock_schema = mocker.MagicMock()
    mocker.patch.object(
        mock_schema,
        "get_components_by_path",
        return_value=range(len(model_element_uris)),
    )
    add_orphan_mock = mocker.patch.object(mock_schema, "add_orphan_elements")

    actual = modelldcatno_factory._resolve_recursive_reference("ref", mock_schema)

    object_creator_mock.assert_called()
    add_orphan_mock.assert_called_once_with([orphan])
    assert actual == component


@pytest.mark.unit
def test_resolve_recursive_reference_returns_single_element_without_adding_orphans(
    mocker: MockerFixture,
) -> None:
    """Returns only referenced component, adding no orphans to schema.."""
    component = mocker.MagicMock(spec=ModelElement)
    model_element_uris = [component, None, None, None]

    object_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        side_effect=model_element_uris,
    )

    mock_schema = mocker.MagicMock()
    mocker.patch.object(
        mock_schema,
        "get_components_by_path",
        return_value=range(len(model_element_uris)),
    )
    add_orphan_mock = mocker.patch.object(mock_schema, "add_orphan_elements")

    actual = modelldcatno_factory._resolve_recursive_reference("ref", mock_schema)

    object_creator_mock.assert_called()
    add_orphan_mock.assert_not_called()
    assert actual == component


@pytest.mark.unit
def test_resolve_recursive_reference_returns_uri(mocker: MockerFixture,) -> None:
    """Returns only referenced component, adding no orphans to schema."""
    component = mocker.MagicMock(spec=URI)
    model_element_uris = [None, None, None, component]

    object_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        side_effect=model_element_uris,
    )

    mock_schema = mocker.MagicMock()
    mocker.patch.object(
        mock_schema,
        "get_components_by_path",
        return_value=range(len(model_element_uris)),
    )
    add_orphan_mock = mocker.patch.object(mock_schema, "add_orphan_elements")

    actual = modelldcatno_factory._resolve_recursive_reference("ref", mock_schema)

    object_creator_mock.assert_called()
    add_orphan_mock.assert_not_called()
    assert actual == component


@pytest.mark.unit
def test_resolve_recursive_reference_returns_none(mocker: MockerFixture,) -> None:
    """Returns None if no elements are created or resolved."""
    model_element_uris = [None, None, None]

    object_creator_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        side_effect=model_element_uris,
    )

    mock_schema = mocker.MagicMock()
    mocker.patch.object(
        mock_schema,
        "get_components_by_path",
        return_value=range(len(model_element_uris)),
    )
    add_orphan_mock = mocker.patch.object(mock_schema, "add_orphan_elements")

    actual = modelldcatno_factory._resolve_recursive_reference("ref", mock_schema)

    object_creator_mock.assert_called()
    add_orphan_mock.assert_not_called()
    assert actual is None


@pytest.mark.unit
def test_creators_returns_already_parsed_components(mocker: MockerFixture) -> None:
    """Test element and property creators returns identifier of parsed components."""
    identifier = "identifier"
    mock_schema = mocker.MagicMock()
    mocker.patch.object(
        mock_schema, "get_parsed_component_uri", return_value=identifier
    )

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier

    assert (
        modelldcatno_factory.create_model_element(mock_component, mock_schema)
        == identifier
    )
    assert (
        modelldcatno_factory.create_model_property(mock_component, mock_schema)
        == identifier
    )


@pytest.mark.unit
def test_invalid_component_returns_no_element_or_property(
    mocker: MockerFixture,
) -> None:
    """Test that empty component returns no element or property."""
    mock_schema = mocker.MagicMock()
    mocker.patch.object(mock_schema, "get_parsed_component_uri", return_value=None)

    mock_component = mocker.MagicMock()
    mock_component.description = None
    mock_component.enum = None
    mock_component.exclusive_maximum = None
    mock_component.exclusive_minimum = None
    mock_component.format = None
    mock_component.items = None
    mock_component.max_length = None
    mock_component.maximum = None
    mock_component.min_length = None
    mock_component.minimum = None
    mock_component.one_of = None
    mock_component.pattern = None
    mock_component.specializes = None
    mock_component.title = None
    mock_component.type = None
    mock_component.ref = None
    mock_component.properties = None

    assert (
        modelldcatno_factory.create_model_element(mock_component, mock_schema) is None
    )
    assert (
        modelldcatno_factory.create_model_property(mock_component, mock_schema) is None
    )


@pytest.mark.unit
def test_returns_correct_type_of_ref(mocker: MockerFixture) -> None:
    """Test that reference type is correctly returned."""
    mock_component = mocker.MagicMock(spec=Component)
    mock_component.type = "string"

    mock_schema = mocker.MagicMock()
    mocker.patch.object(
        mock_schema, "get_components_by_path", return_value=mock_component
    )

    assert modelldcatno_factory._determine_ref_type("test", mock_schema) == "string"


@pytest.mark.unit
def test_create_valid_identifier(mocker: MockerFixture) -> None:
    """Test that valid attributes produces expeceted identifier."""
    title = "title"
    component_path = "components/schemas"
    base_uri = "http://uri.com"
    complete_path = f"{component_path}#{title}"

    mock_schema = mocker.MagicMock()
    mock_schema.base_uri = base_uri

    expected = f"{base_uri}/{component_path}#{title}"
    actual = modelldcatno_factory._create_identifier(complete_path, mock_schema)

    assert expected == actual


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit
def test_creates_valid_object_type(mocker: MockerFixture) -> None:
    """Test that ObjectTypes are correctly created."""
    identifier = "identifier"
    title = {None: "title"}
    description = {None: "description"}
    child_identifier = "child_identifier"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.properties = [mocker.MagicMock()]

    mock_schema = mocker.MagicMock()

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_property",
        return_value=child_identifier,
    )

    expected = ObjectType(identifier)
    expected.title = title
    expected.description = description
    expected.has_property = [child_identifier]

    actual = modelldcatno_factory._create_object_type(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
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

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_property",
        return_value=has_property_identifier,
    )

    expected = SimpleType(identifier)
    expected.title = title
    expected.description = description
    expected.pattern = pattern
    expected.min_length = 0
    expected.max_length = 10
    expected.has_property = [has_property_identifier]

    actual = modelldcatno_factory._create_simple_type(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
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

    expected = SimpleType(identifier)
    expected.min_exclusive = 0
    expected.max_exclusive = 10

    actual = modelldcatno_factory._create_simple_type(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
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

    expected = SimpleType(identifier)
    expected.min_inclusive = 0
    expected.max_inclusive = 10

    actual = modelldcatno_factory._create_simple_type(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
def test_creates_valid_primitive_simple_type(mocker: MockerFixture) -> None:
    """Test that primitve SimpleTypes are correctly created."""
    identifier = "identifier"
    type = "string"

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.type = type
    mock_component.format = None

    expected = SimpleType(identifier)
    expected.identifier = identifier
    expected.title = {None: type}
    expected.type_definition_reference = TYPE_DEFINITION_REFERENCE.get(type)

    actual = modelldcatno_factory._create_primitive_simple_type(mock_component)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
def test_create_code_list(mocker: MockerFixture) -> None:
    """Code Lists are correctly created and and code elements added to orphan graph."""
    identifier = "identifier"
    title = {None: "title"}
    description = {None: "description"}
    enum = ["1", "2", "3"]

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.title = title
    mock_component.description = description
    mock_component.enum = enum

    mock_schema = mocker.MagicMock()
    add_orphan_mock = mocker.patch.object(mock_schema, "add_orphan_elements")

    expected = CodeList(identifier)
    expected.identifier = identifier
    expected.title = title
    expected.description = description

    create_code_element_mock = mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_code_element", side_effect=enum
    )

    actual = modelldcatno_factory._create_code_list(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)
    create_code_element_mock.assert_called()
    add_orphan_mock.assert_called_once_with(enum)


@pytest.mark.unit
def test_create_code_element(mocker: MockerFixture) -> None:
    """Test that Code Elements are correctly created."""
    identifier = "identifier"
    notation = "notation"
    parent = "code_list_uri"

    expected = CodeElement(identifier)
    expected.notation = notation
    expected.in_scheme = [parent]

    mocker.patch(
        "jsonschematordf.modelldcatnofactory._create_identifier",
        return_value=identifier,
    )

    mock_schema = mocker.MagicMock()

    actual = modelldcatno_factory._create_code_element(notation, parent, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
def test_creates_specialization_property(mocker: MockerFixture) -> None:
    """Tests creation of Specialization model property."""
    specialiation_identifier = "specialiation_identifier"
    simple_type_identifier = "simple_type_identifier"

    mock_component = mocker.MagicMock()
    mock_component.identifier = specialiation_identifier
    mock_component.specializes = mocker.MagicMock()

    mock_schema = mocker.MagicMock()

    expected = Specialization(specialiation_identifier)
    expected.has_general_concept = simple_type_identifier

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        return_value=simple_type_identifier,
    )

    actual = modelldcatno_factory._create_specialization_property(
        mock_component, mock_schema
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
def test_creates_attribute_model_property(mocker: MockerFixture) -> None:
    """Test that attribute properties are correctly created."""
    attribute_identifier = "identifier"
    simple_type_identifier = "simple_identifier"
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
    mock_component.enum = None

    mock_schema = mocker.MagicMock()

    expected = Attribute(attribute_identifier)
    expected.title = title
    expected.description = description
    expected.max_occurs = max_occurs
    expected.min_occurs = min_occurs
    expected.has_simple_type = simple_type_identifier

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        return_value=simple_type_identifier,
    )

    actual = modelldcatno_factory._create_attribute_property(
        mock_component, mock_schema
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
def test_attribute_creates_code_list(mocker: MockerFixture) -> None:
    """Attributes create code list if enum is present."""
    identifier = "identifier"
    simple_type_identifier = "simple_type_identifier"
    code_list_identifier = "code_list_identifier"
    type = "string"
    enum = ["1", "2", "3"]

    mock_component = mocker.MagicMock()
    mock_component.identifier = identifier
    mock_component.type = type
    mock_component.enum = enum
    mock_component.title = None
    mock_component.description = None
    mock_component.max_occurs = None
    mock_component.min_occurs = None

    mock_schema = mocker.MagicMock()

    expected = Attribute(identifier)
    expected.has_simple_type = simple_type_identifier
    expected.has_value_from = code_list_identifier

    mocker.patch(
        "jsonschematordf.modelldcatnofactory.create_model_element",
        side_effect=[simple_type_identifier, code_list_identifier],
    )

    actual = modelldcatno_factory._create_attribute_property(
        mock_component, mock_schema
    )

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit
def test_creates_role_property(mocker: MockerFixture) -> None:
    """Test that role properties are correctly created."""
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

    actual = modelldcatno_factory._create_role_property(mock_component, mock_schema)

    g1 = Graph().parse(data=expected.to_rdf(), format="turtle")
    g2 = Graph().parse(data=actual.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)
