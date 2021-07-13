# Pretty-yarrrml2rml
The tool translates mapping rules in RML from YARRRML serialization to RDF turtle in a pretty and interpreatable way for humans. The translation is based on [RML]((https://rml.io/specs/rml/ "RML Spec") and [YARRRML]((https://rml.io/yarrrml/spec/ "YARRRML Spec") specifications.

## Limitations:
We are working on inlcuding the following features which are not yet implemented:
- Translation to [R2RML](https://www.w3.org/TR/r2rml)
- [Named graphs](https://www.w3.org/TR/r2rml/#named-graphs) from R2RML
- Functions included using the [FnO](https://fno.io/) Ontology

## Execution
In order to execute the code run you can download de PyPi module:
```bash
python3 -m pip install pretty-yarrrml2rml
python3 -m pretty_yarrrml2rml -m path_to_input_yarrrml.yml -o path_to_output_rml.rml
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



