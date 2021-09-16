"""Exceptions module."""


from typing import Optional


class ComponentAlreadyExistsException(Exception):
    """Exception for collision in parsed components."""

    def __init__(self, msg: Optional[str] = None) -> None:
        """Inits the exception."""
        Exception.__init__(self, msg)
        self.msg = msg
