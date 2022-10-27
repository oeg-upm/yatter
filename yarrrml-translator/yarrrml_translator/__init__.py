import logging, coloredlogs
from .constants import *
from .mapping import add_prefix, add_mapping
from .source import get_initial_sources, add_source, generate_database_connections, add_table
from .subject import add_subject
from .predicateobject import add_predicate_object_maps
from rdflib import Graph

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s,%(msecs)03d | %(levelname)s: %(message)s')


def translate(yarrrml_data, mapping_format=RML_URI):
    logger.info("Translating YARRRML mapping to [R2]RML")

    list_initial_sources = get_initial_sources(yarrrml_data)
    rml_mapping = [add_prefix(yarrrml_data)]
    rml_mapping.extend(generate_database_connections(yarrrml_data))
    try:
        for mapping in yarrrml_data.get(YARRRML_MAPPINGS):
            if mapping_format == R2RML_URI:
                source_list = add_table(yarrrml_data, mapping, list_initial_sources)
            else:
                source_list = add_source(yarrrml_data, mapping, list_initial_sources)
            subject_list = add_subject(yarrrml_data, mapping)
            pred = add_predicate_object_maps(yarrrml_data, mapping, mapping_format)
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

        logger.info("RML content is created!")
        rml_mapping_string = "".join(rml_mapping)
        try:
            graph = Graph()
            graph.parse(data=rml_mapping_string, format="turtle")
            logger.info("Mapping has been syntactically validated.")
        except Exception as e:
            logger.error("ERROR: There is a syntactic error in the generated mapping")
            logger.error(str(e))
            return None
    except Exception as e:
        logger.error("ERROR: The YARRRML mapping has not been translated")
        logger.error(str(e))
        return None

    logger.info("Translation has finished successfully.")

    return rml_mapping_string


def inverse_translation(rdf_mapping, mapping_format=RML_URI):
    return ""
