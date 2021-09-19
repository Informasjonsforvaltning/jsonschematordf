"""Pytests."""
from typing import Dict

import jsonschematordf.componentfactory as component_factory


def test_component_creator_sets_all_fields_correctly() -> None:
    """Test that ComponentFactory returns Component with correct attributes set."""
    path = "#/path"
    type = "type"
    title = "title"
    description = "description"
    pattern = "pattern"
    format = "format"
    required = ["required"]
    enum = ["enum"]
    minimum = 0
    maximum = 1
    exclusive_minimum = False
    exclusive_maximum = True
    min_length = 0
    max_length = 1
    min_items = 0
    max_items = 1
    items = {"description": "items_test"}
    properties = {"property_title": {"description": "property_description"}}
    all_of = [{"title": "allOf"}]
    one_of = [{"title": "oneOf"}]
    ref = "#/path/test"

    json_schema_representation = {
        "type": type,
        "title": title,
        "description": description,
        "pattern": pattern,
        "format": format,
        "required": required,
        "enum": enum,
        "minimum": minimum,
        "maximum": maximum,
        "exclusiveMinimum": exclusive_minimum,
        "exclusiveMaximum": exclusive_maximum,
        "minLength": min_length,
        "maxLength": max_length,
        "minItems": min_items,
        "maxItems": max_items,
        "items": items,
        "properties": properties,
        "allOf": all_of,
        "oneOf": one_of,
        "$ref": ref,
    }

    child_path = f"{path}/{title}"

    component = component_factory.create_component(path, json_schema_representation)

    assert component.path == path
    assert component.type == type
    assert component.title == {None: title}
    assert component.complete_path == f"/path#{title}"
    assert component.description == {None: description}
    assert component.pattern == pattern
    assert component.format == format
    assert component.required == required
    assert component.enum == enum
    assert component.minimum == minimum
    assert component.maximum == maximum
    assert component.exclusive_minimum == exclusive_minimum
    assert component.exclusive_maximum == exclusive_maximum
    assert component.min_length == min_length
    assert component.max_length == max_length
    assert component.min_items == min_items
    assert component.max_items == max_items
    assert component.items == component_factory.create_component(
        child_path, {**items, "title": "items"}
    )
    assert component.properties == [
        component_factory.create_component(
            f"{path}/{title}",
            {
                **properties.get("property_title", {}),
                "title": "property_title",
                "required": required,
            },
        )
    ]
    assert component.all_of == [
        component_factory.create_component(child_path, component)
        for component in all_of
    ]
    assert component.one_of == [
        component_factory.create_component(child_path, component)
        for component in one_of
    ]
    assert component.ref == ref


def test_componentfactory_correctly_sets_multiplicities_correctly() -> None:
    """Test that multiplicities are correctly inferred."""
    path = "#/path"
    title = "title"

    min_one_max_one = component_factory.create_component(
        path, {"title": title, "required": [title]}
    )

    assert min_one_max_one._min_occurs == 1
    assert min_one_max_one._max_occurs == 1

    min_zero_max_multi = component_factory.create_component(path, {"type": "array"})

    assert min_zero_max_multi.min_occurs == 0
    assert min_zero_max_multi.max_occurs == "*"

    max_from_max_items = component_factory.create_component(
        path, {"type": "array", "maxItems": 100}
    )

    assert max_from_max_items.max_occurs == 100


def test_componentfactory_returns_component_for_each_type() -> None:
    """Test that one Component per type is created."""
    path = "#/path"
    types = ["type1", "type2"]
    json_schema_representation = {"type": types}

    components = component_factory.create_components(path, json_schema_representation)

    assert len(components) == 2
    assert components[0].type == types[0] and components[1].type == types[1]


def test_componentfactory_returns_component_for_empty_schema() -> None:
    """Test that one Component per type is created."""
    path = "#/path"
    json_schema_representation: Dict = {}

    components = component_factory.create_components(path, json_schema_representation)

    assert len(components) == 1
