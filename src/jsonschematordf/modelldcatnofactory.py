"""ModelldcatnoFactory module."""
from typing import Optional

from datacatalogtordf.exceptions import InvalidURIError
from datacatalogtordf.uri import URI
from modelldcatnotordf.modelldcatno import (
    ModelElement,
    ModelProperty,
    ObjectType,
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
    """Create Specialization model property. TODO."""
    identifier = _create_identifier(component, schema)
    if component.complete_path:
        schema.add_parsed_component(component.complete_path, identifier)

    primitive_simple_type = _create_primitive_simple_type(component, schema)

    specialization = Specialization(identifier)
    if primitive_simple_type:
        specialization.has_general_concept = primitive_simple_type

    return specialization
