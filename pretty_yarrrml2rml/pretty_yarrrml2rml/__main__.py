import sys
import yaml
import pretty_yarrrml2rml


def write_results(rml_mapping):
    if len(sys.argv) == 1:
        rml_output_path = input("Name the path for the output file:")
    else:
        rml_output_path = sys.argv[4]

    rml_output_file = open(rml_output_path, "w")
    rml_output_file.write(rml_mapping)
    rml_output_file.close()

    print("Validating the generated RDF file with RDFLib")


def run_parsing_system_inputs():
    if len(sys.argv) == 1:
        file = input("Introduce the .yml file you want to convert to RML")
        with open(file) as f:
            yaml_data = yaml.safe_load(f)

    elif len(sys.argv) == 5 and sys.argv[1] == "-i" and sys.argv[3] == "-o":
        with open(sys.argv[2]) as f:
            yaml_data = yaml.safe_load(f)
    else:
        sys.tracebacklimit = 0
        raise Exception(
            "\n####################################\nERROR: Wrong argument input. You can:"
            "\n-Use no arguments\n-Use arguments (in this order): -i yarrrml.yml -o mapping.rml.ttl"
            "\n####################################\n")

    return yaml_data


yarrrml_data = run_parsing_system_inputs()

rml_content = pretty_yarrrml2rml.translate(yarrrml_data)

write_results(rml_content)
