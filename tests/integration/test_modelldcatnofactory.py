"""Pytests."""
# flake8: noqa
import pytest
from pytest_mock.plugin import MockerFixture
from rdflib.graph import Graph

from jsonschematordf.modelldcatnofactory import create_model_element
from jsonschematordf.schema import Schema
from jsonschematordf.utils import add_elements_to_graph
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
        modelldcatno:hasSimpleType <http://uri.com/#string> .

    <http://uri.com/mock_uri_1> a modelldcatno:Specialization ;
        modelldcatno:hasGeneralConcept <http://uri.com/#string> .

    <http://uri.com/#string> a modelldcatno:SimpleType ;
        dct:title "string" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_object_type_role_property() -> None:
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


@pytest.mark.integration
def test_object_array_property() -> None:
    """Test object array creation."""
    in_dict = {
        "KommuneResultat": {
            "type": "object",
            "properties": {
                "erstatter": {"items": {"$ref": "#/Kommune"}, "type": "array"}
            },
        },
        "Kommune": {"type": "object"},
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/KommuneResultat")

    modelldcatno_representation = create_model_element(components[0], schema)
    assert modelldcatno_representation is not None

    expected = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://uri.com/#KommuneResultat> a modelldcatno:ObjectType ;
        dct:title "KommuneResultat" ;
        modelldcatno:hasProperty <http://uri.com/KommuneResultat#erstatter> .

    <http://uri.com/#Kommune> a modelldcatno:ObjectType ;
        dct:title "Kommune" .

    <http://uri.com/KommuneResultat#erstatter> a modelldcatno:Role ;
        dct:title "erstatter" ;
        xsd:maxOccurs "*" ;
        modelldcatno:hasObjectType <http://uri.com/#Kommune> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_simple_type_array_property(mocker: MockerFixture) -> None:
    """Test simple type array creation."""
    in_dict = {
        "KommuneResultat": {
            "type": "object",
            "properties": {
                "erstatter": {"items": {"$ref": "#/Kommune"}, "type": "array"}
            },
        },
        "Kommune": {"type": "string"},
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/KommuneResultat")

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

    <http://uri.com/#KommuneResultat> a modelldcatno:ObjectType ;
        dct:title "KommuneResultat" ;
        modelldcatno:hasProperty <http://uri.com/KommuneResultat#erstatter> .

    <http://uri.com/#Kommune> a modelldcatno:SimpleType ;
        dct:title "Kommune" ;
        modelldcatno:hasProperty <http://uri.com/mock_uri_0> .

    <http://uri.com/#string> a modelldcatno:SimpleType ;
        dct:title "string" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .

    <http://uri.com/KommuneResultat#erstatter> a modelldcatno:Attribute ;
        dct:title "erstatter" ;
        xsd:maxOccurs "*" ;
        modelldcatno:hasSimpleType <http://uri.com/#Kommune> .

    <http://uri.com/mock_uri_0> a modelldcatno:Specialization ;
        modelldcatno:hasGeneralConcept <http://uri.com/#string> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_nested_objects() -> None:
    """Test handling of nested objects."""
    in_dict = {
        "KommuneResultat": {
            "properties": {
                "code": {"format": "int32", "type": "integer"},
                "data": {
                    "required": ["kommune"],
                    "type": "object",
                    "properties": {
                        "erstatter": {"items": {"$ref": "#/Kommune"}, "type": "array"},
                        "erstattetav": {
                            "items": {"$ref": "#/Kommune"},
                            "type": "array",
                        },
                        "kommune": {"$ref": "#/Kommune", "type": "object"},
                    },
                },
            },
            "required": ["code", "data"],
            "type": "object",
        },
        "Kommune": {"type": "object"},
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/KommuneResultat")

    modelldcatno_representation = create_model_element(components[0], schema)
    assert modelldcatno_representation is not None

    expected = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://uri.com/#KommuneResultat> a modelldcatno:ObjectType ;
        dct:title "KommuneResultat" ;
        modelldcatno:hasProperty <http://uri.com/KommuneResultat#code>,
            <http://uri.com/KommuneResultat#data> .

    <http://uri.com/#int32> a modelldcatno:SimpleType ;
        dct:title "int32" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#integerschema> .

    <http://uri.com/KommuneResultat#code> a modelldcatno:Attribute ;
        dct:title "code" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        xsd:minOccurs 1 ;
        modelldcatno:hasSimpleType <http://uri.com/#int32> .

    <http://uri.com/KommuneResultat#data> a modelldcatno:Role ;
        dct:title "data" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        xsd:minOccurs 1 ;
        modelldcatno:hasObjectType <http://uri.com/KommuneResultat/data#data> .

    <http://uri.com/KommuneResultat/data#data> a modelldcatno:ObjectType ;
        dct:title "data" ;
        modelldcatno:hasProperty <http://uri.com/KommuneResultat/data#erstatter>,
            <http://uri.com/KommuneResultat/data#erstattetav>,
            <http://uri.com/KommuneResultat/data#kommune> .

    <http://uri.com/KommuneResultat/data#erstatter> a modelldcatno:Role ;
        dct:title "erstatter" ;
        xsd:maxOccurs "*" ;
        modelldcatno:hasObjectType <http://uri.com/#Kommune> .

    <http://uri.com/KommuneResultat/data#erstattetav> a modelldcatno:Role ;
        dct:title "erstattetav" ;
        xsd:maxOccurs "*" ;
        modelldcatno:hasObjectType <http://uri.com/#Kommune> .

    <http://uri.com/KommuneResultat/data#kommune> a modelldcatno:Role ;
        dct:title "kommune" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        xsd:minOccurs 1 ;
        modelldcatno:hasObjectType <http://uri.com/#Kommune> .

    <http://uri.com/#Kommune> a modelldcatno:ObjectType ;
        dct:title "Kommune" .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_multiplicity(mocker: MockerFixture) -> None:
    """Test handling of array multiplicity."""
    in_dict = {
        "Account": {
            "type": "object",
            "properties": {
                "links": {
                    "type": "array",
                    "items": {"$ref": "#/Link"},
                    "minItems": 0,
                    "maxItems": 10,
                }
            },
        },
        "Link": {"type": "string"},
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/Account")

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

    <http://uri.com/#Account> a modelldcatno:ObjectType ;
        dct:title "Account" ;
        modelldcatno:hasProperty <http://uri.com/Account#links> .

    <http://uri.com/#Link> a modelldcatno:SimpleType ;
        dct:title "Link" ;
        modelldcatno:hasProperty <http://uri.com/mock_uri_0> .

    <http://uri.com/#string> a modelldcatno:SimpleType ;
        dct:title "string" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .

    <http://uri.com/Account#links> a modelldcatno:Attribute ;
        dct:title "links" ;
        xsd:maxOccurs "10"^^xsd:nonNegativeInteger ;
        modelldcatno:hasSimpleType <http://uri.com/#Link> .

    <http://uri.com/mock_uri_0> a modelldcatno:Specialization ;
        modelldcatno:hasGeneralConcept <http://uri.com/#string> .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = Graph().parse(data=modelldcatno_representation.to_rdf(), format="turtle")

    assert_isomorphic(g1, g2)


@pytest.mark.integration
def test_code_list_and_element(mocker: MockerFixture) -> None:
    """Test code list and element creation."""
    in_dict = {
        "Alphabet": {
            "type": "object",
            "properties": {"letters": {"type": "string", "enum": ["A", "B", "C"]}},
        }
    }
    schema = Schema(BASE_URI, in_dict)
    components = schema.get_components_by_path("#/Alphabet")

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=mock_uri_generator(BASE_URI),
    )

    modelldcatno_representation = create_model_element(components[0], schema)
    assert modelldcatno_representation is not None

    collected_graph = Graph()
    collected_graph.parse(data=modelldcatno_representation.to_rdf(), format="turtle")
    collected_graph.parse(
        data=add_elements_to_graph(Graph(), schema.orphan_elements).serialize(
            format="turtle"
        ),
        format="turtle",
    )

    expected = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://uri.com/#Alphabet> a modelldcatno:ObjectType ;
        dct:title "Alphabet" ;
        modelldcatno:hasProperty <http://uri.com/Alphabet#letters> .

    <http://uri.com/mock_uri_1> a modelldcatno:CodeElement ;
        skos:inScheme <http://uri.com/Alphabet/letters#letters> ;
        skos:notation "A" .

    <http://uri.com/mock_uri_2> a modelldcatno:CodeElement ;
        skos:inScheme <http://uri.com/Alphabet/letters#letters> ;
        skos:notation "B" .

    <http://uri.com/mock_uri_3> a modelldcatno:CodeElement ;
        skos:inScheme <http://uri.com/Alphabet/letters#letters> ;
        skos:notation "C" .

    <http://uri.com/#string> a modelldcatno:SimpleType ;
        dct:title "string" ;
        modelldcatno:typeDefinitionReference <https://www.w3.org/2019/wot/json-schema#stringschema> .

    <http://uri.com/Alphabet#letters> a modelldcatno:Attribute ;
        dct:title "letters" ;
        xsd:maxOccurs "1"^^xsd:nonNegativeInteger ;
        modelldcatno:hasSimpleType <http://uri.com/#string> ;
        modelldcatno:hasValueFrom <http://uri.com/Alphabet/letters#letters> .

    <http://uri.com/Alphabet/letters#letters> a modelldcatno:CodeList ;
        dct:title "letters" .
    """

    g1 = Graph().parse(data=expected, format="turtle")
    g2 = collected_graph

    assert_isomorphic(g1, g2)
