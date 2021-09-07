"""ComponentFactory module."""
from typing import Dict

from jsonschematordf.component import Component


class ComponentFactory:
    """Factory class for instantiating Component objects."""

    __slots__ = ()

    def create_component(
        self, path: str, json_schema_representation: Dict
    ) -> Component:
        """Map JSON Schema dict representation to Component."""
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

        return Component(
            path=f"{path}#{title}" if title else path,
            type=[type] if isinstance(type, str) else type,
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
                self.create_component(
                    f"{path}/{title}" if title else path, {**items, "title": "items"}
                )
                if items
                else None
            ),
            properties=[
                self.create_component(
                    f"{path}/{title}",
                    {"title": property_name, **properties.get(property_name, {})},
                )
                for property_name in properties
            ]
            if properties
            else None,
            all_of=(
                [
                    self.create_component(f"{path}/{title}", component)
                    for component in all_of
                ]
                if all_of
                else None
            ),
            one_of=(
                [
                    self.create_component(f"{path}/{title}", component)
                    for component in one_of
                ]
                if one_of
                else None
            ),
            ref=ref,
        )
