
from .constants import *
from .mapping import add_prefix, add_mapping, add_inverse_prefix
from .source import get_initial_sources, add_source, generate_database_connections, add_table, add_inverse_source
from .subject import add_subject
from .predicateobject import add_predicate_object_maps
import rdflib




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
            graph = rdflib.Graph()
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
    yarrrml_mapping = {'prefixes': [], 'mappings': []}
    rdf_mapping.bind('rml', rdflib.term.URIRef(RML_URI))
    rdf_mapping.bind('rr', rdflib.term.URIRef(R2RML_URI))
    rdf_mapping.bind('ql', rdflib.term.URIRef(QL_URI))
    yarrrml_mapping['prefixes'] = add_inverse_prefix(rdf_mapping)
    query = f'SELECT ?triplesMap WHERE {{ ?triplesMap {RDF_TYPE} {R2RML_TRIPLES_MAP} . }} '
    triples_map = [tm[rdflib.Variable('triplesMap')] for tm in rdf_mapping.query(query).bindings]

    for tm in triples_map:
        tm_text = tm.split("/")[-1]
        yarrrml_tm = {tm_text: {}}
        source = add_inverse_source(tm, rdf_mapping, mapping_format)
        yarrrml_tm[tm_text] = source
        query = f'SELECT ?subject  WHERE {{ <{tm}> {R2RML_SUBJECT} ?subject . }} '
        subject = [tm[rdflib.Variable('subject')] for tm in rdf_mapping.query(query).bindings][0]
        # ToDo: generate the subject from its id

        query = f'SELECT ?predicateObjectMap  WHERE {{ <{tm}> {R2RML_PREDICATE_OBJECT_MAP} ?predicateObjectMap . }} '
        poms = [tm[rdflib.Variable('predicateObjectMap')] for tm in rdf_mapping.query(query).bindings]
        # ToDo: generate the poms from their id

        yarrrml_mapping['mappings'].append(yarrrml_tm)

    return ""
