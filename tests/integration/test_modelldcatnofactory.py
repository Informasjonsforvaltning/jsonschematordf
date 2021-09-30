"""Pytests."""
# flake8: noqa

import pytest
from pytest_mock.plugin import MockerFixture
from rdflib.graph import Graph

from jsonschematordf.modelldcatnofactory import create_model_element
from jsonschematordf.schema import Schema
from tests.testutils import assert_isomorphic, mock_uri_generator


BASE_URI = "http://uri.com"


@pytest.mark.integration
def test_object_type_attribute_property(mocker: MockerFixture) -> None:
    """Test object attribute creation."""
    in_dict = {
        "Eiendom": {
            "properties": {
                "erstatter": {"type": "string"},
                "eiendomAddress": {"$ref": "#/Address"},
            }
        },
        "Address": {"type": "string"},
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/Eiendom")

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=mock_uri_generator(BASE_URI),
    )

    modelldcatno_representation = create_model_element(components[0], schema)
    assert modelldcatno_representation is not None

    expected = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://uri.com/#Eiendom> a modelldcatno:ObjectType ;
            dct:title "Eiendom" ;
            modelldcatno:hasProperty <http://uri.com/Eiendom#eiendomAddress>,
                <http://uri.com/Eiendom#erstatter> .

        <http://uri.com/#Address> a modelldcatno:SimpleType ;
            dct:title "Address" ;
            modelldcatno:hasProperty <http://uri.com/mock_uri_1> .

        <http://uri.com/Eiendom#eiendomAddress> a modelldcatno:Attribute ;
            dct:title "eiendomAddress" ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
            modelldcatno:hasSimpleType <http://uri.com/#Address> .

        <http://uri.com/Eiendom#erstatter> a modelldcatno:Attribute ;
            dct:title "erstatter" ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
            modelldcatno:hasSimpleType <http://uri.com/string> .

        <http://uri.com/mock_uri_1> a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept <http://uri.com/string> .

        <http://uri.com/string> a modelldcatno:SimpleType ;
            dct:title "string" ;
            modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_object_type_role_property(mocker: MockerFixture) -> None:
    """Test object role creation."""
    in_dict = {
        "EiendomResultat": {
            "properties": {
                "data": {"$ref": "#/Eiendom"},
                "address": {"type": "object"},
            },
            "required": ["data"],
            "type": "object",
        },
        "Eiendom": {"type": "object"},
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/EiendomResultat")

    modelldcatno_representation = create_model_element(components[0], schema)
    assert modelldcatno_representation is not None

    expected = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://uri.com/#EiendomResultat> a modelldcatno:ObjectType ;
        dct:title "EiendomResultat" ;
        modelldcatno:hasProperty <http://uri.com/EiendomResultat#address>,
            <http://uri.com/EiendomResultat#data> .

    <http://uri.com/#Eiendom> a modelldcatno:ObjectType ;
        dct:title "Eiendom" .

    <http://uri.com/EiendomResultat#address> a modelldcatno:Role ;
        dct:title "address" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        modelldcatno:hasObjectType <http://uri.com/EiendomResultat/address#address> .

    <http://uri.com/EiendomResultat#data> a modelldcatno:Role ;
        dct:title "data" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        xsd:minOccurs 1 ;
        modelldcatno:hasObjectType <http://uri.com/#Eiendom> .

    <http://uri.com/EiendomResultat/address#address> a modelldcatno:ObjectType ;
        dct:title "address" .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)
