"""
Tests for yatter jelly integration for input output.
For PR #99: feat(cli): support for Jelly format for input/output
"""

import pytest
import types
from pathlib import Path

from rdflib import Graph
from ruamel.yaml import YAML
import rdflib
import importlib
import importlib.util
pytest.importorskip("pyjelly")
from yatter.cli import write_results, parse_inputs, translate, inverse_translation

def _mimic_args(**kwargs):
    return types.SimpleNamespace(**kwargs)

def test_parse_inputs_acc_jelly(tmp_path: Path):

    output_mapping_path = str(tmp_path / 'output_mapping.yml')
    args = _mimic_args(input_mapping_path = 'test/jelly-tests/jelly_mapping_test_jelly.jelly', output_mapping_path = output_mapping_path, merge_mapping = None, format=None)

    parsed_format, parsed_data = parse_inputs(args)

    assert isinstance(parsed_data, rdflib.Graph)
    assert isinstance(parsed_format, str)

def test_parse_inputs_acc_ttl(tmp_path: Path):
    output_mapping_path = str(tmp_path / 'output_mapping.yml')

    args = _mimic_args(input_mapping_path = 'test/jelly-tests/jelly_mapping_test_ttl.ttl', output_mapping_path = output_mapping_path, merge_mapping = None, format=None)

    parsed_format, parsed_data = parse_inputs(args)

    assert isinstance(parsed_data, rdflib.Graph)
    assert isinstance(parsed_format, str)

def test_parse_inputs_invalid_extension(tmp_path: Path):
    output_mapping_path = str(tmp_path / 'output_mapping.yml')

    args = _mimic_args(input_mapping_path = 'test/jelly-tests/jelly_mapping_test_txt.txt', output_mapping_path = output_mapping_path, merge_mapping = None, format=None)

    with pytest.raises(Exception) as excinfo:
        parsed_format, parsed_data = parse_inputs(args)

    assert "Change your mapping extension to a valid one" in excinfo.value.args[0]

def test_write_results_roundtrip_to_jelly(tmp_path: Path):
    output_mapping_path = str(tmp_path / 'output_mapping.jelly')
    args = _mimic_args(input_mapping_path='test/jelly-tests/jelly_mapping_test_yml.yml',
                       output_mapping_path=output_mapping_path, merge_mapping=None,
                       format=None)

    parsed_format, parsed_data = parse_inputs(args)

    mapping_content = translate(parsed_data, parsed_format)

    assert isinstance(mapping_content, str)

    write_results(args, mapping_content)

    g = Graph()
    g.parse(output_mapping_path, format='jelly')

    assert isinstance(g, rdflib.Graph)


def test_write_results_roundtrip_to_yaml(tmp_path: Path):
    output_mapping_path = str(tmp_path / 'output_mapping.yml')
    args = _mimic_args(input_mapping_path='test/jelly-tests/jelly_mapping_test_jelly.jelly',
                       output_mapping_path=output_mapping_path, merge_mapping=None,
                       format=None)

    parsed_format, parsed_data = parse_inputs(args)

    mapping_content = inverse_translation(parsed_data, parsed_format)

    assert isinstance(mapping_content, dict)

    write_results(args, mapping_content)

    yaml_mapping_f = YAML(typ='safe', pure=True)
    yaml_mapping = yaml_mapping_f.load(open(output_mapping_path))
    assert isinstance(yaml_mapping, dict)
    assert yaml_mapping == mapping_content



def test_write_results_roundtrip_to_ttl(tmp_path: Path):
    output_mapping_path = str(tmp_path / 'output_mapping.ttl')
    args = _mimic_args(input_mapping_path='test/jelly-tests/jelly_mapping_test_yml.yml',
                       output_mapping_path=output_mapping_path, merge_mapping=None,
                       format=None)

    parsed_format, parsed_data = parse_inputs(args)

    mapping_content = translate(parsed_data, parsed_format)

    assert isinstance(mapping_content, str)

    write_results(args, mapping_content)

    g = Graph()
    g.parse(output_mapping_path, format='turtle')

    assert isinstance(g, rdflib.Graph)
