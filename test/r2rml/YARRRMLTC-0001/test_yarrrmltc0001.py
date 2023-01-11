__author__ = "David Chaves-Fraga"
__credits__ = ["David Chaves-Fraga"]

__license__ = "Apache-2.0"
__maintainer__ = "David Chaves-Fraga"
__email__ = "david.chaves@upm.es"


import os
import _ruamel_yaml as yaml
import yarrrml_translator
from rdflib.graph import Graph
from rdflib import compare
R2RML_URI = 'http://www.w3.org/ns/r2rml#'


def test_yarrrmltc0001():
    expected_mapping = Graph()
    expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.ttl'), format="ttl")

    translated_mapping = Graph()
    mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.yml')
    translated_mapping.parse(data=yarrrml_translator.translate(yaml.safe_load(open(mapping_path)), mapping_format=R2RML_URI), format="ttl")

    assert compare.isomorphic(expected_mapping, translated_mapping)
