import yaml
import sys

from rdflib import Graph
import constants
import mapping as mapping_mod
import source as source_mod
import subject as subject_mod
import predicateobject as predicate_object_mod


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


def open_inputs(yarrml_path):
    with open(yarrml_path) as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data


def write_results(rml_content):
    if len(sys.argv) == 1:
        rml_output_path = input("Name the path for the output file:")
    else:
        rml_output_path = sys.argv[4]

    rml_output_file = open(rml_output_path, "w")
    rml_output_file.write(rml_content)
    rml_output_file.close()

    print("Validating the generated RDF file with RDFLib")
    try:
        graph = Graph()
        graph.parse(rml_output_path, format="turtle")
    except Exception as e:
        print("------------------------ERROR-------------------------------")
        print("File not created: " + str(e))
        sys.exit()

def translate(yarrrml_data):
    print("------------------------START TRANSLATING YARRRML TO RML-------------------------------")
    list_initial_sources = source_mod.get_initial_sources(yarrrml_data)
    rml_mapping = [mapping_mod.add_prefix(yarrrml_data)]
    try:
        for mapping in yarrrml_data.get(constants.YARRRML_MAPPINGS):
            subject_list = subject_mod.add_subject(yarrrml_data, mapping)
            source_list = source_mod.add_source(yarrrml_data, mapping, list_initial_sources)
            pred = predicate_object_mod.add_predicate_object_maps(yarrrml_data, mapping)
            it = 0
            for source in source_list:
                for subject in subject_list:
                    map_aux = mapping_mod.add_mapping(mapping, it)
                    if type(source) is list:
                        rml_mapping.append(map_aux + source[0] + subject + pred + source[1])
                    else:
                        rml_mapping.append(map_aux + source + subject + pred)
                    rml_mapping[len(rml_mapping)-1] = rml_mapping[len(rml_mapping)-1][:-2]
                    rml_mapping.append(".\n\n\n")
                    it = it + 1

        print("RML content successfully created!")
    except Exception as e:
        print("------------------------ERROR-------------------------------")
        print("RML content not generated: "+str(e))
        sys.exit()

    return "".join(rml_mapping)


if __name__ == "__main__":
    yarrrml_data = run_parsing_system_inputs()
    rml_content = translate(yarrrml_data)
    write_results(rml_content)

    print("------------------------END TRANSLATION-------------------------------")
