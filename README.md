# yarrrml-translator

![GitHub](https://img.shields.io/github/license/oeg-upm/yarrrml-translator?style=flat)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7024501.svg)](https://doi.org/10.5281/zenodo.7024501)
[![PyPI](https://img.shields.io/pypi/v/yarrrml-translator?style=flat)](https://pypi.org/project/yarrrml-translator)
![GitHub Release Date](https://img.shields.io/github/release-date/oeg-upm/yarrrml-translator)

The tool translates mapping rules from YARRRML in a turtle-based serialization of RML or R2RML. The translation is based 
on the [RML](https://rml.io/specs/rml/) and [YARRRML](https://rml.io/yarrrml/spec/) specifications.

## Installation:
```
pip install yarrrml-translator
```

## Execution from CLI
To execute from command line run the following:

- From YARRRML to \[R2\]RML
```bash
python3 -m yarrrml_translator -i path_to_input_yarrrml.yml -o path_to_rdf_mapping.ttl [-f R2RML]
```
`-f R2RML` is an optional parameter for translating input YARRRML into R2RML

- From \[R2\]RML to YARRRML 
```bash
python3 -m yarrrml_translator -i path_to_input_rdf_mapping.ttl -o path_to_output_yarrrml.yml [-f R2RML]
```
`-f R2RML` is an optional parameter for translating input R2RML into YARRRML

- Merging mappings based on TriplesMap id (keys of each TriplesMap should be disjoint):
```bash
python3 -m yarrrml_translator -m yarrrml_mapping1.yaml yarrrml_mapping2.yaml [..] -o path_to_output_yarrrml.yml
```

## Execution as a library

If you want to include the module in your implementation:
- for translating **YARRRML mapping** to **RML mappings** (and inverse):
```python
import yarrrml_translator
from ruamel.yaml import YAML
# YARRRML to RML
yaml = YAML(typ='safe', pure=True)
rml_content = yarrrml_translator.translate(yaml.load(open("path-to-yarrrml")))
# RML to YARRRML
yarrrml_content = yarrrml_translator.inverse_translate("rdf_mapping_content")
```
- for translating **YARRRML mappings** to **R2RML mappings** (and inverse):
```python
import yarrrml_translator
from ruamel.yaml import YAML

R2RML_URI = 'http://www.w3.org/ns/r2rml#'
# YARRRML to R2RML
yaml = YAML(typ='safe', pure=True)
rml_content = yarrrml_translator.translate(yaml.load(open("path-to-yarrrml")), mapping_format=R2RML_URI)
# R2RML to YARRRML
yarrrml_content = yarrrml_translator.inverse_translate("rdf_mapping_content", mapping_format=R2RML_URI)
```
- for merging TriplesMap based on id:
```python
import yarrrml_translator
list_yarrrml_mappings = ["content_mapping_yarrrml1", "content_mapping_yarrrml1"]
yarrrml_content = yarrrml_translator.merge_mappings(list_yarrrml_mappings)
```


## Specifications conformant:

These are the following specifications used by the translation process:
- YARRRML: https://github.com/kg-construct/yarrrml-spec (Proper website soon)
- R2RML: https://www.w3.org/TR/r2rml/ 
- RML: https://rml.io/spec 
- RML-star: https://w3id.org/kg-construct/rml-star 
- RML-Target: https://rml.io/specs/rml-target/ 
- RML-FNML: https://kg-construct.github.io/fnml-spec/

## Authors
Ontology Engineering Group:
- [David Chaves-Fraga](mailto:david.chaves@upm.es)
- Marino González García (Final bachelor thesis - Systematic Testing)
- Luis López Piñero (Final bachelor thesis - v0.1)



