"""JsonSchemaToRDF module."""

import yaml


def parsejsonschema(schema: str) -> None:
    """Parse JSON Schema."""
    yaml.safe_load(schema)
