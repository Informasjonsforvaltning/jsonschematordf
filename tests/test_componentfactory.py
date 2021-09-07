"""Pytests."""
from jsonschematordf.componentfactory import ComponentFactory


def test_componentfactory_returns_correct_component() -> None:
    """Test that ComponentFactory returns Component with correct attributes set."""
    path = "#/path"
    type = ["type"]
    title = "title"
    description = "description"
    pattern = "pattern"
    format = "format"
    required = ["required"]
    enum = ["enum"]
    minimum = 0
    maximum = 1
    exclusive_minimum = 0
    exclusive_maximum = 1
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

    component_path = f"{path}#{title}"
    child_path = f"{path}/{title}"

    factory = ComponentFactory()

    component = factory.create_component(path, json_schema_representation)

    assert component.path == component_path
    assert component.type == type
    assert component.title == {None: title}
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
    assert component.items == factory.create_component(
        child_path, {**items, "title": "items"}
    )
    assert component.properties == [
        factory.create_component(
            f"{path}/{title}",
            {**properties.get("property_title", {}), "title": "property_title"},
        )
    ]
    assert component.all_of == [
        factory.create_component(child_path, component) for component in all_of
    ]
    assert component.one_of == [
        factory.create_component(child_path, component) for component in one_of
    ]
    assert component.ref == ref
