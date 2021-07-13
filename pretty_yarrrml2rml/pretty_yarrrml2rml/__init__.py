import pretty_yarrrml2rml.constants as constants
import pretty_yarrrml2rml.mapping as mapping_mod
import pretty_yarrrml2rml.source as source_mod
import pretty_yarrrml2rml.subject as subject_mod
import pretty_yarrrml2rml.predicateobject as predicate_object_mod
import os
from rdflib import Graph


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
                    rml_mapping[len(rml_mapping) - 1] = rml_mapping[len(rml_mapping) - 1][:-2]
                    rml_mapping.append(".\n\n\n")
                    it = it + 1

        print("RML content successfully created!\n Starting the validation with RDFLib....")
        rml_mapping_string = "".join(rml_mapping)
        try:
            rml_output_file = open("tmp.nt", "w")
            rml_output_file.write(rml_mapping_string)
            rml_output_file.close()
            graph = Graph()
            graph.parse("tmp.nt", format="turtle")
            if os.path.exists("tmp.nt"):
                os.remove("tmp.nt")
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
