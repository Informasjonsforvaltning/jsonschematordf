"""ComponentFactory module."""
from typing import Dict, List, Optional

from jsonschematordf.component import Component
from jsonschematordf.types.enums import EMPTY_PATH


def create_components(
    path: Optional[str], json_schema_representation: Dict
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


def create_component(
    path: Optional[str], json_schema_representation: Dict
) -> Component:
    """Map JSON Schema dict representation to Component."""
    component_path = path if path else EMPTY_PATH
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

    if type == "array":
        max_occurs = str(max_items) if max_items else "*"
    else:
        max_occurs = "1"

    if title is not None and required is not None and title in required:
        min_occurs = "1"
    else:
        min_occurs = "0"

    child_path = f"{path}/{title}" if title else None

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


def new_from_component(
    component: Component,
    path: Optional[str] = None,
    type: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    pattern: Optional[str] = None,
    format: Optional[str] = None,
    required: Optional[List[str]] = None,
    enum: Optional[List[str]] = None,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    exclusive_minimum: Optional[bool] = None,
    exclusive_maximum: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    items: Optional[Component] = None,
    properties: Optional[List[Component]] = None,
    all_of: Optional[List[Component]] = None,
    one_of: Optional[List[Component]] = None,
    ref: Optional[str] = None,
    max_occurs: Optional[str] = None,
    min_occurs: Optional[str] = None,
) -> Component:
    """Create new component from existing, replacing chosen properties."""
    return Component(
        path=path if path else component.path,
        type=type if type else component.type,
        title={None: title} if title else component.title,
        description={None: description} if description else component.description,
        pattern=pattern if pattern else component.pattern,
        format=format if format else component.format,
        required=required if required else component.required,
        enum=enum if enum else component.enum,
        minimum=minimum if minimum else component.minimum,
        maximum=maximum if maximum else component.maximum,
        exclusive_minimum=exclusive_minimum
        if exclusive_minimum
        else component.exclusive_minimum,
        exclusive_maximum=exclusive_maximum
        if exclusive_maximum
        else component.exclusive_maximum,
        min_length=min_length if min_length else component.min_length,
        max_length=max_length if max_length else component.max_length,
        min_items=min_items if min_items else component.min_items,
        max_items=max_items if max_items else component.max_items,
        items=items if items else component.items,
        properties=properties if properties else component.properties,
        all_of=all_of if all_of else component.all_of,
        one_of=one_of if one_of else component.one_of,
        ref=ref if ref else component.ref,
        max_occurs=max_occurs if max_occurs else component.max_occurs,
        min_occurs=min_occurs if min_occurs else component.min_occurs,
    )
