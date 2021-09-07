"""Component module."""
from typing import Dict, List, Optional


class Component:
    """Utility class representing a JSON Schema component."""

    __slots__ = (
        "_path",
        "_type",
        "_title",
        "_description",
        "_pattern",
        "_format",
        "_required",
        "_enum",
        "_minimum",
        "_maximum",
        "_exclusive_minimum",
        "_exclusive_maximum",
        "_min_length",
        "_max_length",
        "_min_items",
        "_max_items",
        "_items",
        "_properties",
        "_all_of",
        "_one_of",
        "_ref",
    )

    _path: str
    _type: Optional[List[str]]
    _title: Optional[Dict[None, str]]
    _description: Optional[Dict[None, str]]
    _pattern: Optional[str]
    _format: Optional[str]
    _required: Optional[List[str]]
    _enum: Optional[List[str]]
    _minimum: Optional[int]
    _maximum: Optional[int]
    _exclusive_minimum: Optional[int]
    _exclusive_maximum: Optional[int]
    _min_length: Optional[int]
    _max_length: Optional[int]
    _min_items: Optional[int]
    _max_items: Optional[int]
    _items: Optional["Component"]
    _properties: Optional[List["Component"]]
    _all_of: Optional[List["Component"]]
    _one_of: Optional[List["Component"]]
    _ref: Optional[str]

    def __init__(
        self,
        path: str,
        type: Optional[List[str]] = None,
        title: Optional[Dict[None, str]] = None,
        description: Optional[Dict[None, str]] = None,
        pattern: Optional[str] = None,
        format: Optional[str] = None,
        required: Optional[List[str]] = None,
        enum: Optional[List[str]] = None,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        exclusive_minimum: Optional[int] = None,
        exclusive_maximum: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        items: Optional["Component"] = None,
        properties: Optional[List["Component"]] = None,
        all_of: Optional[List["Component"]] = None,
        one_of: Optional[List["Component"]] = None,
        ref: Optional[str] = None,
    ) -> None:
        """Constructor for Component object."""
        self._path = path
        self._type = type
        self._title = title
        self._description = description
        self._pattern = pattern
        self._format = format
        self._required = required
        self._enum = enum
        self._minimum = minimum
        self._maximum = maximum
        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum
        self._min_length = min_length
        self._max_length = max_length
        self._min_items = min_items
        self._max_items = max_items
        self._items = items
        self._properties = properties
        self._all_of = all_of
        self._one_of = one_of
        self._ref = ref

    def __eq__(self, o: object) -> bool:
        """Evaluate equality between Component and other object."""
        return (
            isinstance(o, Component)
            and self.path == o.path
            and self.type == o.type
            and self.title == o.title
            and self.description == o.description
            and self.pattern == o.pattern
            and self.format == o.format
            and self.required == o.required
            and self.enum == o.enum
            and self.minimum == o.minimum
            and self.maximum == o.maximum
            and self.exclusive_minimum == o.exclusive_minimum
            and self.exclusive_maximum == o.exclusive_maximum
            and self.min_length == o.min_length
            and self.max_length == o.max_length
            and self.min_items == o.min_items
            and self.max_items == o.max_items
            and self.items == o.items
            and self.properties == o.properties
            and self.all_of == o.all_of
            and self.one_of == o.one_of
            and self.ref == o.ref
        )

    @property
    def path(self) -> str:
        """Getter for path."""
        return self._path

    @property
    def type(self) -> Optional[List[str]]:
        """Getter for type."""
        return self._type

    @property
    def title(self) -> Optional[Dict[None, str]]:
        """Getter for title."""
        return self._title

    @property
    def description(self) -> Optional[Dict[None, str]]:
        """Getter for description."""
        return self._description

    @property
    def pattern(self) -> Optional[str]:
        """Getter for pattern."""
        return self._pattern

    @property
    def format(self) -> Optional[str]:
        """Getter for format."""
        return self._format

    @property
    def required(self) -> Optional[List[str]]:
        """Getter for required."""
        return self._required

    @property
    def enum(self) -> Optional[List[str]]:
        """Getter for enum."""
        return self._enum

    @property
    def minimum(self) -> Optional[int]:
        """Getter for minimum."""
        return self._minimum

    @property
    def maximum(self) -> Optional[int]:
        """Getter for maximum."""
        return self._maximum

    @property
    def exclusive_minimum(self) -> Optional[int]:
        """Getter for exclusive_minimum."""
        return self._exclusive_minimum

    @property
    def exclusive_maximum(self) -> Optional[int]:
        """Getter for exclusive_maximum."""
        return self._exclusive_maximum

    @property
    def min_length(self) -> Optional[int]:
        """Getter for min_length."""
        return self._min_length

    @property
    def max_length(self) -> Optional[int]:
        """Getter for max_length."""
        return self._max_length

    @property
    def min_items(self) -> Optional[int]:
        """Getter for min_items."""
        return self._min_items

    @property
    def max_items(self) -> Optional[int]:
        """Getter for max_items."""
        return self._max_items

    @property
    def items(self) -> Optional["Component"]:
        """Getter for items."""
        return self._items

    @property
    def properties(self) -> Optional[List["Component"]]:
        """Getter for properties."""
        return self._properties

    @property
    def all_of(self) -> Optional[List["Component"]]:
        """Getter for all_of."""
        return self._all_of

    @property
    def one_of(self) -> Optional[List["Component"]]:
        """Getter for one_of."""
        return self._one_of

    @property
    def ref(self) -> Optional[str]:
        """Getter for ref."""
        return self._ref