import yaml
import sys
from lib import mapping as mapping_mod
from lib import source as source_mod
from lib import subject as subject_mod
from lib import predicateobject as predicate_object_mod


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
            "\n-Use no arguments\n-Use arguments: -m YARRRMLfile -o RMLFile"
            "\n####################################\n")
    return yaml_data

def open_inputs(yarrml_path):
    with open(yarrml_path) as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data


def write_results(rml_content):
    if len(sys.argv) == 1:
        rml_output_path = open(input("Name the path for the output file:"), "a")
    else:
        rml_output_path = open(sys.argv[3],"a")

    rml_output_path.write(rml_content)


def translate(yarrrml_data):
    print("------------------------START TRANSLATING RML-------------------------------")
    list_initial_sources = source_mod.getInitialSources(yarrrml_data)
    final = mapping_mod.addPrefix(yarrrml_data)
    try:
        for mapp in yarrrml_data.get("mappings"):
            subject_list = subject_mod.addSubject(yarrrml_data, mapp)
            source_list = source_mod.addSource(yarrrml_data, mapp, list_initial_sources)
            pred = predicate_object_mod.addPredicateObject(yarrrml_data, mapp)
            it = 0
            for source in source_list:
                for subject in subject_list:
                    map = mapping_mod.addMapping(yarrrml_data, mapp, it)
                    if type(source) is list:
                        final += map + source[0] + subject + pred + source[1]
                    else:
                        final += map + source + subject + pred
                    final = final[:-3]
                    final += ".\n\n\n"
                    it = it + 1

    except Exception as e:
        print(str(e))
        print("------------------------END RML-------------------------------")
        print("FILE NOT SUCCESSFULY CREATED")
        #sys.exit()

    return final


if __name__ == "__main__":
    yarrrml_data = run_parsing_system_inputs()
    rml_content = translate(yarrrml_data)
    write_results(rml_content)

    print("------------------------END RML-------------------------------")
    print("FILE SUCCESSFULY CREATED!")
