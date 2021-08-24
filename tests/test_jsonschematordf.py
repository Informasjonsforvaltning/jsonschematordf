"""Pytests."""
from jsonschematordf import jsonschematordf


def test_read_valid_schema() -> None:
    """Test read valid schema does not raise error."""
    jsonschematordf.parsejsonschema("""{"test":"string"}""")
    assert True
