"""Pytests."""
from jsonschematordf.component import Component


def test_component_sets_fields_correctly() -> None:
    """Test intializing Component object."""
    path = "#/path"
    type = ["type"]
    title = {None: "title"}
    description = {None: "description"}
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
    items = Component(
        "#/path/title", title={None: "items"}, description={None: "items_description"}
    )
    properties = [
        Component(
            "#/path/title",
            title={None: "properties"},
            description={None: "properties_description"},
        )
    ]
    all_of = [
        Component(
            "#/path/title",
            title={None: "all_of"},
            description={None: "all_of_description"},
        )
    ]
    one_of = [
        Component(
            "#/path/title",
            title={None: "one_of"},
            description={None: "one_of_description"},
        )
    ]
    ref = "#/path/test"

    component = Component(
        path,
        type,
        title,
        description,
        pattern,
        format,
        required,
        enum,
        minimum,
        maximum,
        exclusive_minimum,
        exclusive_maximum,
        min_length,
        max_length,
        min_items,
        max_items,
        items,
        properties,
        all_of,
        one_of,
        ref,
    )

    assert component.path == path
    assert component.type == type
    assert component.title == title
    assert component.description == description
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
    assert component.items == items
    assert component.properties == properties
    assert component.all_of == all_of
    assert component.one_of == one_of
    assert component.ref == ref
