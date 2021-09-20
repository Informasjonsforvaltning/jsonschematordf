"""ModelldcatnoFactory module."""
from typing import Optional

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
import jsonschematordf.componentfactory as component_factory
from jsonschematordf.schema import Schema
from jsonschematordf.types.constants import TYPE_DEFINITION_REFERENCE
from jsonschematordf.types.enums import EMPTY_PATH


def create_model_property(
    component: Component, schema: Schema
) -> Optional[ModelProperty]:
    """TODO Create modelldcatno property component for JSON Schema Component."""
    return None


def create_model_element(
    component: Component, schema: Schema
) -> Optional[ModelElement]:
    """TODO Create modelldcatno element component for JSON Schema Component."""
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
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    object_type = ObjectType(identifier)
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
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    simple_type = SimpleType(identifier)
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
        specialization_component = component_factory.new_from_component(
            component, path=component.path + "/specializes"
        )
        simple_type.has_property = [
            _create_specialization_property(specialization_component, schema)
        ]

    return simple_type


def _create_primitive_simple_type(component: Component, schema: Schema) -> SimpleType:
    """Create primitive global simple type based on format or type."""
    primitive_component = component_factory.create_component(
        EMPTY_PATH,
        {
            "title": component.format if component.format else component.type,
            "type": component.type,
        },
    )
    identifier = _create_identifier(primitive_component, schema)
    if primitive_component.complete_path:
        schema.add_parsed_component(primitive_component.complete_path, identifier)

    simple_type = SimpleType(identifier)
    simple_type.title = primitive_component.title

    if type_reference := TYPE_DEFINITION_REFERENCE.get(primitive_component.type):
        simple_type.type_definition_reference = type_reference

    return simple_type


def _create_specialization_property(
    component: Component, schema: Schema
) -> Specialization:
    """Create Specialization model property."""
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    specialization = Specialization(identifier)
    specialization.has_general_concept = _create_primitive_simple_type(
        component, schema
    )

    return specialization


def _create_attribute_property(component: Component, schema: Schema) -> Attribute:
    """Create Attribute model property."""
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    attribute = Attribute(identifier)
    attribute.title = component.title
    attribute.description = component.description
    attribute.max_occurs = component.max_occurs
    attribute.min_occurs = component.min_occurs
    if component.type or component.format:
        attribute.has_simple_type = _create_primitive_simple_type(component, schema)

    return attribute


def _create_choice_property(component: Component, schema: Schema) -> Attribute:
    """Create Choice model property."""
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    choice = Choice(identifier)
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
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    array = Role(identifier)
    array.title = component.title
    array.description = component.description
    array.max_occurs = component.max_occurs
    array.min_occurs = component.min_occurs
    array.has_object_type = (
        create_model_element(component.items, schema) if component.items else None
    )

    return array


def _create_simple_type_array_property(component: Component, schema: Schema) -> Role:
    """Create simple type array model property."""
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    array = Attribute(identifier)
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
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    role = Role(identifier)
    role.title = component.title
    role.description = component.description
    role.max_occurs = component.max_occurs
    role.min_occurs = component.min_occurs
    role.has_object_type = create_model_element(component, schema)

    return role
