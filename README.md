# Pretty-yarrrml2rml

![GitHub](https://img.shields.io/github/license/oeg-upm/pretty-yarrrml2rml?style=flat)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7024501.svg)](https://doi.org/10.5281/zenodo.7024501)
![PyPI](https://img.shields.io/pypi/v/pretty-yarrrml2rml?style=flat)
![GitHub Release Date](https://img.shields.io/github/release-date/oeg-upm/pretty-yarrrml2rml)

The tool translates mapping rules from YARRRML in a pretty turtle-based serialization of RML. The translation is based 
on [RML]((https://rml.io/specs/rml/ "RML Spec") and [YARRRML]((https://rml.io/yarrrml/spec/ "YARRRML Spec") specifications.

## Limitations:
We are working on inlcuding the following features which are not yet implemented:
- Translation to [R2RML](https://www.w3.org/TR/r2rml)
- [Named graphs](https://www.w3.org/TR/r2rml/#named-graphs) from R2RML
- Functions included using the [FnO](https://fno.io/) Ontology

## Execution
In order to execute the code run you can download de PyPi module:
```bash
python3 -m pip install pretty-yarrrml2rml
python3 -m pretty_yarrrml2rml -i path_to_input_yarrrml.yml -o path_to_output_rml.rml
```

If you want to include the module in your implementation:
```python
import pretty_yarrrml2rml
import yaml

rml_content = pretty_yarrrml2rml.translate(yaml.safe_load(open("path-to-yarrrml")))
```

## Authors
Ontology Engineering Group - Data Integration:
- [David Chaves-Fraga](mailto:david.chaves@upm.es)
- Luis López Piñero (Final bachelor thesis - v0.1)



