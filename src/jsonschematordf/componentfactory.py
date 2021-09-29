"""ComponentFactory module."""
from typing import Dict, List, Optional

from jsonschematordf.component import Component
from jsonschematordf.types.enums import EMPTY_PATH


def create_components(
    path: List[str], json_schema_representation: Dict
) -> List[Component]:
    """Creates component for each associated type."""
    component_types = json_schema_representation.get("type")
    if isinstance(component_types, list):
        return [
            create_component(path, {**json_schema_representation, "type": type})
            for type in component_types
        ]
    else:
        return [create_component(path, json_schema_representation)]


def create_component(path: List[str], json_schema_representation: Dict) -> Component:
    """Map JSON Schema dict representation to Component."""
    component_path = path
    type = json_schema_representation.get("type")
    title = json_schema_representation.get("title")
    description = json_schema_representation.get("description")
    pattern = json_schema_representation.get("pattern")
    format = json_schema_representation.get("format")
    required = json_schema_representation.get("required")
    enum = json_schema_representation.get("enum")
    minimum = json_schema_representation.get("minimum")
    maximum = json_schema_representation.get("maximum")
    exclusive_minimum = json_schema_representation.get("exclusiveMinimum")
    exclusive_maximum = json_schema_representation.get("exclusiveMaximum")
    min_length = json_schema_representation.get("minLength")
    max_length = json_schema_representation.get("maxLength")
    min_items = json_schema_representation.get("minItems")
    max_items = json_schema_representation.get("maxItems")
    items = json_schema_representation.get("items")
    properties = json_schema_representation.get("properties")
    all_of = json_schema_representation.get("allOf")
    one_of = json_schema_representation.get("oneOf")
    ref = json_schema_representation.get("$ref")

    if type == "array" or one_of:
        max_occurs: Optional[str] = str(max_items) if max_items else "*"
    else:
        max_occurs = "1"

    if title is not None and required is not None and title in required:
        min_occurs = 1
    else:
        min_occurs = 0

    child_path = [*path, title] if title else [EMPTY_PATH]

    return Component(
        path=component_path,
        type=type,
        title={None: title} if title else None,
        description={None: description} if description else None,
        pattern=pattern,
        format=format,
        required=required,
        enum=enum,
        minimum=minimum,
        maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
        min_length=min_length,
        max_length=max_length,
        min_items=min_items,
        max_items=max_items,
        items=(
            create_component(child_path, {**items, "title": "items"}) if items else None
        ),
        properties=[
            create_component(
                child_path,
                {
                    "title": property_name,
                    "required": required,
                    **properties.get(property_name, {}),
                },
            )
            for property_name in properties
        ]
        if properties
        else None,
        all_of=(
            [create_component(child_path, component) for component in all_of]
            if all_of
            else None
        ),
        one_of=(
            [create_component(child_path, component) for component in one_of]
            if one_of
            else None
        ),
        ref=ref,
        max_occurs=max_occurs,
        min_occurs=min_occurs,
    )
