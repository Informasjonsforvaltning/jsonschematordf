"""ModelldcatnoFactory module."""
from typing import Optional, Union

from datacatalogtordf.uri import URI
from modelldcatnotordf.modelldcatno import (
    Attribute,
    Choice,
    CodeElement,
    CodeList,
    ModelElement,
    ModelProperty,
    ObjectType,
    Role,
    SimpleType,
    Specialization,
)

from jsonschematordf.component import Component
from jsonschematordf.schema import Schema
from jsonschematordf.types.constants import TYPE_DEFINITION_REFERENCE
from jsonschematordf.types.enums import (
    CHOICE,
    CODE_LIST,
    EMPTY_PATH,
    EXTERNAL_REFERENCE,
    OBJECT_ARRAY,
    OBJECT_TYPE,
    PRIMITIVE_SIMPLE_TYPE,
    RECURSIVE_REFERENCE,
    SIMPLE_TYPE,
    SIMPLE_TYPE_ARRAY,
    SPECIALIZES,
)
from jsonschematordf.utils import add_to_path, determine_reference_type


def create_model_property(
    component: Component, schema: Schema
) -> Optional[Union[ModelProperty, URI]]:
    """Create modelldcatno property component for JSON Schema Component."""
    if parsed_component_uri := schema.get_parsed_component_uri(component.complete_path):
        return parsed_component_uri

    component.identifier = schema.create_identifier(component.complete_path)
    schema.add_parsed_component(component)
    component_type = _determine_component_type(component, schema)

    if component_type == OBJECT_TYPE:
        return _create_role_property(component, schema)
    if (
        component_type == SIMPLE_TYPE
        or component_type == PRIMITIVE_SIMPLE_TYPE
        or component_type == CODE_LIST
    ):
        return _create_attribute_property(component, schema)
    if component_type == CHOICE:
        return _create_choice_property(component, schema)
    if component_type == SPECIALIZES:
        return _create_specialization_property(component, schema)
    if component_type == OBJECT_ARRAY:
        return _create_object_array_property(component, schema)
    if component_type == SIMPLE_TYPE_ARRAY:
        return _create_simple_type_array_property(component, schema)

    return None


def create_model_element(
    component: Component, schema: Schema
) -> Optional[Union[ModelElement, URI]]:
    """Create modelldcatno element component for JSON Schema Component."""
    if parsed_component_uri := schema.get_parsed_component_uri(component.complete_path):
        return parsed_component_uri
    if component.ref:
        return _resolve_component_reference(component.ref, schema)

    component.identifier = schema.create_identifier(component.complete_path)
    schema.add_parsed_component(component)
    component_type = _determine_component_type(component, schema)

    if component_type == OBJECT_TYPE:
        return _create_object_type(component, schema)
    if component_type == SIMPLE_TYPE:
        return _create_simple_type(component, schema)
    if component_type == PRIMITIVE_SIMPLE_TYPE:
        return _create_primitive_simple_type(component, schema)
    if component_type == CODE_LIST:
        return _create_code_list(component, schema)
    return None


def _create_code_element(
    notation: str, parent: CodeList, schema: Schema
) -> CodeElement:
    """Create Code Element."""
    identifier = schema.create_identifier(None)
    code_element = CodeElement(identifier)
    code_element.notation = notation
    code_element.in_scheme = [parent]
    return code_element


def _resolve_component_reference(
    reference: str, schema: Schema
) -> Optional[Union[ModelElement, URI]]:
    """Resolve component reference."""
    reference_type = determine_reference_type(reference)
    if reference_type == RECURSIVE_REFERENCE:
        return _resolve_recursive_reference(reference, schema)
    if reference_type == EXTERNAL_REFERENCE:
        return reference
    return None


def _resolve_recursive_reference(
    ref: str, schema: Schema
) -> Optional[Union[ModelElement, URI]]:
    """Resolve recursive component reference and handle orphans."""
    reference_components = schema.get_components_by_path(ref)

    model_elements = []
    uri = None

    for component in reference_components:
        element = create_model_element(component, schema)
        if isinstance(element, ModelElement) or isinstance(element, CodeList):
            model_elements.append(element)
        if isinstance(element, URI):
            uri = element

    if len(model_elements) > 1:
        first_element, *orphans = model_elements
        schema.add_orphan_elements(orphans)
        return first_element
    elif len(model_elements) == 1:
        return model_elements[0]
    elif uri is not None:
        return uri
    else:
        return None


def _determine_component_type(component: Component, schema: Schema) -> Optional[str]:
    """Determine type of json schema component."""
    ref_type = _determine_ref_type(component.ref, schema) if component.ref else None

    if component.items:
        items_type = _determine_component_type(component.items, schema)
        if items_type == OBJECT_TYPE:
            return OBJECT_ARRAY
        if items_type == SIMPLE_TYPE:
            return SIMPLE_TYPE_ARRAY
    if component.specializes:
        return SPECIALIZES
    if component.one_of:
        return CHOICE
    if component.enum:
        return CODE_LIST
    if component.type == "object" or component.properties:
        return OBJECT_TYPE
    if (
        component.type in TYPE_DEFINITION_REFERENCE.keys()
        or ref_type in TYPE_DEFINITION_REFERENCE.keys()
    ):
        if (
            component.title
            or component.description
            or component.pattern
            or component.min_length
            or component.max_length
            or component.minimum
            or component.exclusive_minimum
            or component.maximum
            or component.exclusive_maximum
        ):
            return SIMPLE_TYPE
        return PRIMITIVE_SIMPLE_TYPE

    return ref_type


def _determine_ref_type(ref: str, schema: Schema) -> Optional[str]:
    """Determine type of referenced schema."""
    reference_type = determine_reference_type(ref)
    if reference_type == RECURSIVE_REFERENCE:
        referenced_components = schema.get_components_by_path(ref)
        if len(referenced_components) >= 1 and isinstance(
            referenced_components[0], Component
        ):
            return _determine_component_type(referenced_components[0], schema)

    elif reference_type == EXTERNAL_REFERENCE:
        return "object"
    return None


def _create_object_type(component: Component, schema: Schema) -> ObjectType:
    """Create object type."""
    object_type = ObjectType(component.identifier)
    object_type.title = component.title
    object_type.description = component.description

    if component.properties:
        model_properties = [
            create_model_property(model_property, schema)
            for model_property in component.properties
        ]
        object_type.has_property = [
            property for property in model_properties if property
        ]

    return object_type


def _create_simple_type(component: Component, schema: Schema) -> SimpleType:
    """Create simple type."""
    simple_type = SimpleType(component.identifier)
    simple_type.title = component.title
    simple_type.description = component.description
    simple_type.pattern = component.pattern
    simple_type.min_length = component.min_length
    simple_type.max_length = component.max_length

    if component.minimum is not None:
        if component.exclusive_minimum:
            simple_type.min_exclusive = component.minimum
        else:
            simple_type.min_inclusive = component.minimum

    if component.maximum is not None:
        if component.exclusive_maximum:
            simple_type.max_exclusive = component.maximum
        else:
            simple_type.max_inclusive = component.maximum

    if component.title and (component.type or component.format):
        primitive_simple_type = Component(
            [EMPTY_PATH], format=component.format, type=component.type
        )
        specialization_component = Component(
            [*component.path, "specializes"], specializes=primitive_simple_type
        )
        specialization_property = create_model_property(
            specialization_component, schema
        )
        simple_type.has_property = (
            [specialization_property] if specialization_property else None
        )

    return simple_type


def _create_primitive_simple_type(component: Component, schema: Schema) -> SimpleType:
    """Create primitive global simple type based on format or type."""
    title = component.format if component.format else component.type

    simple_type = SimpleType(schema.create_identifier("/#" + title if title else None))
    simple_type.title = {None: title} if title else None

    if type_reference := TYPE_DEFINITION_REFERENCE.get(component.type):
        simple_type.type_definition_reference = type_reference

    return simple_type


def _create_code_list(component: Component, schema: Schema) -> CodeList:
    """Create Code List and add Code Elements to orphan graph."""
    code_list = CodeList(component.identifier)
    code_list.title = component.title
    code_list.description = component.description

    if component.enum:
        code_elements = [
            _create_code_element(notation=notation, parent=code_list, schema=schema)
            for notation in component.enum
        ]

        schema.add_orphan_elements(code_elements)

    return code_list


def _create_specialization_property(
    component: Component, schema: Schema
) -> Specialization:
    """Create Specialization model property."""
    specialization = Specialization(component.identifier)
    if component.specializes:
        specialization.has_general_concept = create_model_element(
            component.specializes, schema
        )

    return specialization


def _create_attribute_property(component: Component, schema: Schema) -> Attribute:
    """Create Attribute model property."""
    attribute = Attribute(component.identifier)
    attribute.title = component.title
    attribute.description = component.description
    attribute.max_occurs = component.max_occurs
    attribute.min_occurs = component.min_occurs

    child_path = add_to_path(
        component.path, component.title.get(None) if component.title else None
    )

    contains_simple_type = _determine_component_type(
        component.omit(["enum", "title", "description"]), schema
    ) in [SIMPLE_TYPE, PRIMITIVE_SIMPLE_TYPE]
    contains_code_list = _determine_component_type(component, schema) == CODE_LIST

    if contains_simple_type:
        attribute.has_simple_type = create_model_element(
            component.omit(["enum", "title", "description"], new_path=child_path),
            schema,
        )
    if contains_code_list:
        attribute.has_value_from = create_model_element(
            component.copy(path=child_path), schema
        )

    return attribute


def _create_choice_property(component: Component, schema: Schema) -> Attribute:
    """Create Choice model property."""
    choice = Choice(component.identifier)
    choice.title = component.title
    choice.description = component.description
    choice.max_occurs = component.max_occurs
    choice.min_occurs = component.min_occurs
    if component.one_of:
        one_of_elements = [
            create_model_element(item, schema) for item in component.one_of
        ]
        choice.has_some = [element for element in one_of_elements if element]

    return choice


def _create_object_array_property(component: Component, schema: Schema) -> Role:
    """Create object array model property."""
    array = Role(component.identifier)
    array.title = component.title
    array.description = component.description
    array.max_occurs = component.max_occurs
    array.min_occurs = component.min_occurs
    array.has_object_type = (
        create_model_element(component.items, schema) if component.items else None
    )

    return array


def _create_simple_type_array_property(
    component: Component, schema: Schema
) -> Attribute:
    """Create simple type array model property."""
    array = Attribute(component.identifier)
    array.title = component.title
    array.description = component.description
    array.max_occurs = component.max_occurs
    array.min_occurs = component.min_occurs
    array.has_simple_type = (
        create_model_element(component.items, schema) if component.items else None
    )

    return array


def _create_role_property(component: Component, schema: Schema) -> Role:
    """Create object array model property."""
    role = Role(component.identifier)
    role.title = component.title
    role.description = component.description
    role.max_occurs = component.max_occurs
    role.min_occurs = component.min_occurs

    object_type_path = add_to_path(
        component.path, component.title.get(None) if component.title else None
    )
    role.has_object_type = create_model_element(
        component.copy(path=object_type_path), schema
    )

    return role
