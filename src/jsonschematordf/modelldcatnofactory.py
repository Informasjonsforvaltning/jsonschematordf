"""ModelldcatnoFactory module."""
from typing import Optional, Union

from datacatalogtordf.exceptions import InvalidURIError
from datacatalogtordf.uri import URI
from modelldcatnotordf.modelldcatno import (
    Attribute,
    Choice,
    ModelElement,
    ModelProperty,
    ObjectType,
    Role,
    SimpleType,
    Specialization,
)
from skolemizer import Skolemizer

from jsonschematordf.component import Component
from jsonschematordf.schema import Schema
from jsonschematordf.types.constants import TYPE_DEFINITION_REFERENCE
from jsonschematordf.types.enums import (
    CHOICE,
    EMPTY_PATH,
    OBJECT_ARRAY,
    OBJECT_TYPE,
    PRIMITIVE_SIMPLE_TYPE,
    SIMPLE_TYPE,
    SIMPLE_TYPE_ARRAY,
    SPECIALIZES,
)


def create_model_property(
    component: Component, schema: Schema
) -> Optional[Union[ModelProperty, URI]]:
    """Create modelldcatno property component for JSON Schema Component."""
    if parsed_component_uri := schema.get_parsed_component_uri(component.complete_path):
        return parsed_component_uri

    component.identifier = _create_identifier(component, schema)
    schema.add_parsed_component(component)
    component_type = _determine_component_type(component, schema)

    if component_type == OBJECT_TYPE:
        return _create_role_property(component, schema)
    if component_type == SIMPLE_TYPE:
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

    component.identifier = _create_identifier(component, schema)
    schema.add_parsed_component(component)
    component_type = _determine_component_type(component, schema)

    if component_type == OBJECT_TYPE:
        return _create_object_type(component, schema)
    if component_type == SIMPLE_TYPE:
        return _create_simple_type(component, schema)
    if component_type == PRIMITIVE_SIMPLE_TYPE:
        return _create_primitive_simple_type(component)
    return None


def _determine_component_type(component: Component, schema: Schema) -> Optional[str]:
    """Determine type of json schema component."""
    ref_type = _determine_ref_type(component.ref, schema)

    if component.type == "object" or ref_type == "object":
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
        if component.format:
            return PRIMITIVE_SIMPLE_TYPE
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

    return None


def _determine_ref_type(ref: Optional[str], schema: Schema) -> Optional[str]:
    """Determine type of referenced schema."""
    if ref:
        referenced_component = schema.get_components_by_path(ref)
        if isinstance(referenced_component, Component):
            return referenced_component.type
    return None


def _create_identifier(component: Component, schema: Schema) -> URI:
    """Create identifier for component."""
    if schema.base_uri and component.complete_path:
        try:
            component_uri = f"{schema.base_uri}/{component.complete_path}"
            return URI(component_uri)
        except InvalidURIError:
            pass
    return Skolemizer.add_skolemization()


def _create_object_type(component: Component, schema: Schema) -> ObjectType:
    """Create object type."""
    object_type = ObjectType(component.identifier)
    object_type.title = component.title
    object_type.description = component.description

    if component.properties:
        object_type.has_property = [
            create_model_property(model_property, schema)
            for model_property in component.properties
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
            EMPTY_PATH, format=component.format, type=component.type
        )
        specialization_component = Component(
            component.path + "/specializes", specializes=primitive_simple_type
        )

        simple_type.has_property = [
            create_model_property(specialization_component, schema)
        ]

    return simple_type


def _create_primitive_simple_type(component: Component) -> SimpleType:
    """Create primitive global simple type based on format or type."""
    title = component.format if component.format else component.type

    simple_type = SimpleType(component.identifier)
    simple_type.title = {None: title} if title else None

    if type_reference := TYPE_DEFINITION_REFERENCE.get(component.type):
        simple_type.type_definition_reference = type_reference

    return simple_type


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
    if component.type or component.format:
        attribute.has_simple_type = create_model_element(component, schema)

    return attribute


def _create_choice_property(component: Component, schema: Schema) -> Attribute:
    """Create Choice model property."""
    choice = Choice(component.identifier)
    choice.title = component.title
    choice.description = component.description
    choice.max_occurs = component.max_occurs
    choice.min_occurs = component.min_occurs
    if component.one_of:
        choice.has_some = [
            create_model_element(item, schema) for item in component.one_of
        ]

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
    role.has_object_type = create_model_element(component, schema)

    return role
