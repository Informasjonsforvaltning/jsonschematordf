"""Pytests."""
# flake8: noqa

import pytest
from pytest_mock.plugin import MockerFixture
from rdflib.graph import Graph

from jsonschematordf.modelldcatnofactory import create_model_element
from jsonschematordf.schema import Schema
from tests.testutils import assert_isomorphic


BASE_URI = "http://uri.com"


@pytest.mark.integration
def test_object_type_attribute_property(mocker: MockerFixture) -> None:
    """Test object attribute creation."""
    in_dict = {"Eiendom": {"properties": {"erstatter": {"type": "string"}}}}
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/Eiendom")

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=f"{BASE_URI}/mock_uri",
    )

    modelldcatno_representation = create_model_element(components[0], schema)
    assert modelldcatno_representation is not None

    expected = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://uri.com/#Eiendom> a modelldcatno:ObjectType ;
        dct:title "Eiendom" ;
        modelldcatno:hasProperty <http://uri.com/Eiendom#erstatter> .

    <http://uri.com/Eiendom#erstatter> a modelldcatno:Attribute ;
        dct:title "erstatter" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        modelldcatno:hasSimpleType <http://uri.com/mock_uri> .

    <http://uri.com/mock_uri> a modelldcatno:SimpleType ;
        dct:title "string" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)
