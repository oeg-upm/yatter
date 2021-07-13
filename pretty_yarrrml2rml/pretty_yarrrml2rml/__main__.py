import sys
import pretty_yarrrml2rml

def run_parsing_system_inputs():
    if len(sys.argv) == 1:
        file = input("Introduce the .yml file you want to convert to RML")
        with open(file) as f:
            yaml_data = yaml.safe_load(f)

    elif len(sys.argv) == 5 and sys.argv[1] == "-m" and sys.argv[3] == "-o":
        with open(sys.argv[2]) as f:
            yaml_data = yaml.safe_load(f)
    else:
        sys.tracebacklimit = 0
        raise Exception(
            "\n####################################\nERROR: Wrong argument input. You can:"
            "\n-Use no arguments\n-Use arguments (in this order): -m yarrrml.yml -o mapping.rml.ttl"
            "\n####################################\n")
    return yaml_data


yarrrml_data = run_parsing_system_inputs()

rml_content = pretty_yarrrml2rml.translate(yarrrml_data)

pretty_yarrrml2rml.write_results(rml_content)
