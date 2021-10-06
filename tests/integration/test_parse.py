"""Pytests."""
# flake8: noqa
import pytest
from pytest_mock.plugin import MockerFixture
from rdflib.graph import Graph

from tests.testutils import assert_isomorphic, mock_uri_generator

from jsonschematordf.parse import json_schema_to_graph


BASE_URI = "http://uri.com"


@pytest.mark.integration
def test_graph_creation(mocker: MockerFixture) -> None:
    """Test graph creation."""
    json_schema_string = """{
        "Eiendom":{
            "properties":{
                "erstatter":{
                    "type":"string"
                },
                "propertyCode":{
                    "type":"string",
                    "enum":[
                    "residential",
                    "commercial",
                    "public"
                    ]
                }
            }
        },
        "Address":{
            "type":"string"
        }
    }"""

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=mock_uri_generator(BASE_URI),
    )

    expected = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://uri.com/#Address> a modelldcatno:SimpleType ;
        dct:title "Address" ;
        modelldcatno:hasProperty <http://uri.com/mock_uri_5> .

    <http://uri.com/#Eiendom> a modelldcatno:ObjectType ;
        dct:title "Eiendom" ;
        modelldcatno:hasProperty <http://uri.com/Eiendom#erstatter>,
            <http://uri.com/Eiendom#propertyCode> .

    <http://uri.com/mock_uri_2> a modelldcatno:CodeElement ;
        skos:inScheme <http://uri.com/Eiendom/propertyCode#propertyCode> ;
        skos:notation "residential" .

    <http://uri.com/mock_uri_3> a modelldcatno:CodeElement ;
        skos:inScheme <http://uri.com/Eiendom/propertyCode#propertyCode> ;
        skos:notation "commercial" .

    <http://uri.com/mock_uri_4> a modelldcatno:CodeElement ;
        skos:inScheme <http://uri.com/Eiendom/propertyCode#propertyCode> ;
        skos:notation "public" .

    <http://uri.com/Eiendom#erstatter> a modelldcatno:Attribute ;
        dct:title "erstatter" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        modelldcatno:hasSimpleType <http://uri.com/#string> .

    <http://uri.com/Eiendom#propertyCode> a modelldcatno:Attribute ;
        dct:title "propertyCode" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        modelldcatno:hasSimpleType <http://uri.com/#string> ;
        modelldcatno:hasValueFrom <http://uri.com/Eiendom/propertyCode#propertyCode> .

    <http://uri.com/mock_uri_5> a modelldcatno:Specialization ;
        modelldcatno:hasGeneralConcept <http://uri.com/#string> .

    <http://uri.com/#string> a modelldcatno:SimpleType ;
        dct:title "string" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .

    <http://uri.com/Eiendom/propertyCode#propertyCode> a modelldcatno:CodeList ;
        dct:title "propertyCode" .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = json_schema_to_graph(json_schema_string, BASE_URI)

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_referenced_objects_are_parsed_once(mocker: MockerFixture) -> None:
    """Test that referenced objects appear once and all root elements are parsed."""
    json_schema_string = """{
        "EiendomResultat":{
            "properties":{
                "dataType":{
                    "oneOf":[
                    {
                        "$ref":"#/XML"
                    },
                    {
                        "$ref":"#/CSV"
                    }
                    ]
                },
                "address":{
                    "type":"object"
                }
            },
            "required":[
                "data"
            ],
            "type":"object"
        },
        "Eiendom":{
            "type":"object"
        },
        "XML":{
            "type":"string",
            "description":"XML stands for extensible markup language."
        },
        "CSV":{
            "type":"string",
            "description":"A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values."
        }
    }"""

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=mock_uri_generator(BASE_URI),
    )

    expected = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://uri.com/#Eiendom> a modelldcatno:ObjectType ;
            dct:title "Eiendom" .

        <http://uri.com/#EiendomResultat> a modelldcatno:ObjectType ;
            dct:title "EiendomResultat" ;
            modelldcatno:hasProperty <http://uri.com/EiendomResultat#address>,
                <http://uri.com/EiendomResultat#dataType> .

        <http://uri.com/#CSV> a modelldcatno:SimpleType ;
            dct:description "A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values." ;
            dct:title "CSV" ;
            modelldcatno:hasProperty <http://uri.com/mock_uri_2> .

        <http://uri.com/#XML> a modelldcatno:SimpleType ;
            dct:description "XML stands for extensible markup language." ;
            dct:title "XML" ;
            modelldcatno:hasProperty <http://uri.com/mock_uri_0> .

        <http://uri.com/EiendomResultat#address> a modelldcatno:Role ;
            dct:title "address" ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
            modelldcatno:hasObjectType <http://uri.com/EiendomResultat/address#address> .

        <http://uri.com/EiendomResultat#dataType> a modelldcatno:Choice ;
            dct:title "dataType" ;
            xsd:maxOccurs "*" ;
            modelldcatno:hasSome <http://uri.com/#CSV>,
                <http://uri.com/#XML> .

        <http://uri.com/EiendomResultat/address#address> a modelldcatno:ObjectType ;
            dct:title "address" .

        <http://uri.com/mock_uri_0> a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept <http://uri.com/#string> .

        <http://uri.com/mock_uri_2> a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept <http://uri.com/#string> .

        <http://uri.com/#string> a modelldcatno:SimpleType ;
            dct:title "string" ;
            modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = json_schema_to_graph(json_schema_string, BASE_URI)

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_handles_circular_and_external_references() -> None:
    """Test that circular and external references are handled correctly."""
    json_schema_string = """{
        "One":{
            "type":"object",
            "properties":{
                "oneToTwo":{
                    "$ref":"#/Two"
                },
                "oneToExternal":{
                    "$ref":"http://someuri.com"
                }
            }
        },
        "Two":{
            "type":"object",
            "properties":{
                "twoToOne":{
                    "$ref":"#/One"
                }
            }
        }
    }"""

    expected = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://uri.com/#One> a modelldcatno:ObjectType ;
            dct:title "One" ;
            modelldcatno:hasProperty <http://uri.com/One#oneToExternal>,
                <http://uri.com/One#oneToTwo> .

        <http://uri.com/#Two> a modelldcatno:ObjectType ;
            dct:title "Two" ;
            modelldcatno:hasProperty <http://uri.com/Two#twoToOne> .

        <http://uri.com/One#oneToExternal> a modelldcatno:Role ;
            dct:title "oneToExternal" ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
            modelldcatno:hasObjectType <http://someuri.com> .

        <http://uri.com/One#oneToTwo> a modelldcatno:Role ;
            dct:title "oneToTwo" ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
            modelldcatno:hasObjectType <http://uri.com/#Two> .

        <http://uri.com/Two#twoToOne> a modelldcatno:Role ;
            dct:title "twoToOne" ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
            modelldcatno:hasObjectType <http://uri.com/#One> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = json_schema_to_graph(json_schema_string, BASE_URI)

    assert_isomorphic(g1, g2)
