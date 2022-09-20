# yarrrml-translator

![GitHub](https://img.shields.io/github/license/oeg-upm/yarrrml-translator?style=flat)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7024501.svg)](https://doi.org/10.5281/zenodo.7024501)
![PyPI](https://img.shields.io/pypi/v/yarrrml-translator?style=flat)
![GitHub Release Date](https://img.shields.io/github/release-date/oeg-upm/yarrrml-translator)

The tool translates mapping rules from YARRRML in a turtle-based serialization of RML. The translation is based 
on the [RML](https://rml.io/specs/rml/) and [YARRRML](https://rml.io/yarrrml/spec/) specifications.

## Limitations
We are working on including the following features which are not yet implemented:
- Translation to [R2RML](https://www.w3.org/TR/r2rml)
- Functions using the [FnO](https://fno.io/) Ontology

## Execution

Installation:
```
pip install yarrrml-translator
```

To execute from command line run the following:
```bash
python3 -m yarrrml-translator -i path_to_input_yarrrml.yml -o path_to_output_rml.rml
```

If you want to include the module in your implementation:
```python
import yarrrml-translator
import yaml

rml_content = yarrrml-translator.translate(yaml.safe_load(open("path-to-yarrrml")))
```

## Authors
Ontology Engineering Group - Data Integration:
- [David Chaves-Fraga](mailto:david.chaves@upm.es)
- Luis López Piñero (Final bachelor thesis - v0.1)



