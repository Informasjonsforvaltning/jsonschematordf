"""ParsedSchema module."""
from typing import Iterator, List, Union

from attr import dataclass
from modelldcatnotordf.modelldcatno import CodeElement, ModelElement


@dataclass
class ParsedSchema:
    """A class representing the modelldcatno output of a parsed JSON Schema document."""

    model_elements: List[ModelElement] = []
    orphan_elements: List[Union[ModelElement, CodeElement]] = []

    def __iter__(self) -> Iterator:
        """Returns iterable of class attributes."""
        return iter((self.model_elements, self.orphan_elements))
