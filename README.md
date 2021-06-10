# YARRRML2RML
Repository for the pretty transformation of YARRRML mappings into RML. This parser is based on RML and YARRRML mapping rules which can be seen here:
- [RML Spec](https://rml.io/specs/rml/ "RML Spec")
- [YARRRML Spec](https://rml.io/yarrrml/spec/ "YARRRML Spec")

## Requirements
The only mandatory external library needed to execute the parser is [PyYAML](https://pypi.org/project/PyYAML/ "pyyaml").

## Licensing
YARRRML2RML is licensed under the Apache License, Version 2.0.

## Execution
In order to execute the code run:

``` python
python3 -m pip install -r requirements.txt
python3 main.py -m path_to_input_yarrrml.yml -o path_to_output_rml.rml
```

## Authors
Luis López Piñero


