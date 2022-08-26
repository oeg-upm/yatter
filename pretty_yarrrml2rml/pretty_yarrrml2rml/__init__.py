from .constants import *
from .mapping import add_prefix, add_mapping
from .source import get_initial_sources, add_source, generate_database_connections
from .subject import add_subject
from .predicateobject import add_predicate_object_maps
import os
from rdflib import Graph


def translate(yarrrml_data):
    print("------------------------START TRANSLATING YARRRML TO RML-------------------------------")
    list_initial_sources = get_initial_sources(yarrrml_data)
    rml_mapping = [add_prefix(yarrrml_data)]
    rml_mapping.extend(generate_database_connections(yarrrml_data))
    try:
        for mapping in yarrrml_data.get(YARRRML_MAPPINGS):
            source_list = add_source(yarrrml_data, mapping, list_initial_sources)
            subject_list = add_subject(yarrrml_data, mapping)
            pred = add_predicate_object_maps(yarrrml_data, mapping)
            it = 0
            for source in source_list:
                for subject in subject_list:
                    map_aux = add_mapping(mapping, it)
                    if type(source) is list:
                        rml_mapping.append(map_aux + source[0] + subject + pred + source[1])
                    else:
                        rml_mapping.append(map_aux + source + subject + pred)
                    rml_mapping[len(rml_mapping) - 1] = rml_mapping[len(rml_mapping) - 1][:-2]
                    rml_mapping.append(".\n\n\n")
                    it = it + 1

        print("RML content successfully created!\nStarting the validation with RDFLib....")
        rml_mapping_string = "".join(rml_mapping)
        try:
            rml_output_file = open("tmp.nt", "w")
            rml_output_file.write(rml_mapping_string)
            rml_output_file.close()
            graph = Graph()
            graph.parse("tmp.nt", format="turtle")
            if os.path.exists("tmp.nt"):
                os.remove("tmp.nt")
            print("The mapping in RML was successfully validated.")
        except Exception as e:
            print("------------------------ERROR-------------------------------")
            print("Validating the RDF generated: " + str(e))
            if os.path.exists("tmp.nt"):
                os.remove("tmp.nt")
            return None
    except Exception as e:
        print("------------------------ERROR-------------------------------")
        print("RML content not generated: " + str(e))
        return None

    print("------------------------END TRANSLATION-------------------------------")

    return rml_mapping_string
