__author__ = "Marino Gonzalez Garcia"
__credits__ = ["Marino Gonzalez Garcia"]

__license__ = "Apache-2.0"
__maintainer__ = "Marino Gonzalez Garcia"
__email__ = "marino.gonzalez.garcia@alumnos.upm.es"


import os
import yaml
import yarrrml_translator
from rdflib.graph import Graph
from rdflib import compare
RMLSTAR_URI = 'http://semweb.mmlab.be/ns/rml#'


def test_yarrrmltc0005():
    expected_mapping = Graph()
    expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.rmls.ttl'), format="ttl")

    translated_mapping = Graph()
    mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.yml')
    translated_mapping.parse(data=yarrrml_translator.translate(yaml.safe_load(open(mapping_path)), mapping_format=RMLSTAR_URI), format="ttl")

    assert compare.isomorphic(expected_mapping, translated_mapping)