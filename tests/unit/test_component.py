"""Pytests."""
import pytest

from jsonschematordf.component import Component
from jsonschematordf.types.enums import EMPTY_PATH


@pytest.mark.unit
def test_component_sets_fields_correctly() -> None:
    """Test intializing Component object."""
    path = ["#"]
    type = "type"
    title = {None: "title"}
    complete_path = "/#title"
    description = {None: "description"}
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
    items = Component(
        ["#", "path", "title"],
        title={None: "items"},
        description={None: "items_description"},
    )
    properties = [
        Component(
            ["#", "path", "title"],
            title={None: "properties"},
            description={None: "properties_description"},
        )
    ]
    all_of = [
        Component(
            ["#", "path", "title"],
            title={None: "all_of"},
            description={None: "all_of_description"},
        )
    ]
    one_of = [
        Component(
            ["#", "path", "title"],
            title={None: "one_of"},
            description={None: "one_of_description"},
        )
    ]
    ref = "#/path/test"
    max_occurs = "*"
    min_occurs = 0
    specializes = Component(
        ["#", "path", "title"],
        title={None: "specializes"},
        description={None: "specializes_description"},
    )

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
        max_occurs,
        min_occurs,
        specializes,
    )

    assert component.path == path
    assert component.complete_path == complete_path
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
    assert component.max_occurs == max_occurs
    assert component.min_occurs == min_occurs
    assert component.specializes == specializes


@pytest.mark.unit
def test_complete_path_returns_none_for_missing_title() -> None:
    """Test that complete path is not built without title."""
    path = ["#", "path"]
    component = Component(path)

    assert component.complete_path is None


@pytest.mark.unit
def test_identifier_set_and_get() -> None:
    """Test that identifier can be set and gotten."""
    identifier = "identifier"
    component = Component(["#"])

    assert component.identifier is None

    component.identifier = identifier

    assert component.identifier == identifier


@pytest.mark.unit
def test_omit() -> None:
    """Test Component copy funciton."""
    component = Component(path=["#"], type="string", title={None: "title"})

    assert component.omit(["title"]) == Component(path=["#"], type="string")
    assert component.omit(["path"]).path == [EMPTY_PATH]
    assert component.omit(["title"], new_path=["#", "schema"]).path == ["#", "schema"]


@pytest.mark.unit
def test_copy() -> None:
    """Test Component copy funciton."""
    component = Component(path=["#"], type="string", title={None: "title"})

    new_title = {None: "changed"}
    expected = Component(path=["#"], type="string", title=new_title)

    assert component.copy() == component
    assert component.copy(title=new_title) == expected
