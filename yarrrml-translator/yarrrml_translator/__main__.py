import sys
import yaml
from . import translate
from .constants import RML_URI, R2RML_URI


def write_results(rml_mapping):
    if len(sys.argv) == 1:
        rml_output_path = input("Name the path for the output file:")
    else:
        rml_output_path = sys.argv[sys.argv.index("-o") + 1]

    rml_output_file = open(rml_output_path, "w")
    rml_output_file.write(rml_mapping)
    rml_output_file.close()

    print("Output mapping saved")


def run_parsing_system_inputs():
    mapping_format = RML_URI
    if len(sys.argv) == 1:
        file = input("Introduce the .yml file you want to convert to RML")
        with open(file) as f:
            yaml_data = yaml.safe_load(f)

    elif (len(sys.argv) == 5 or len(sys.argv) == 7) and "-i" in sys.argv and "-o" in sys.argv:
        with open(sys.argv[sys.argv.index("-i") + 1]) as f:
            yaml_data = yaml.safe_load(f)
        if "-f" in sys.argv:
            if sys.argv[sys.argv.index("-f") + 1] == "R2RML":
                mapping_format = R2RML_URI
    else:
        sys.tracebacklimit = 0
        raise Exception(
            "\n####################################\nERROR: Wrong argument input. You can:"
            "\n-Use no arguments\n-Use arguments (in this order): -i yarrrml.yml -o mapping.rml.ttl"
            "\n####################################\n")

    return mapping_format, yaml_data


mapping_format, yarrrml_data = run_parsing_system_inputs()

rml_content = translate(yarrrml_data, mapping_format)

write_results(rml_content)
