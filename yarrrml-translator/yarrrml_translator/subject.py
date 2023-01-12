from .constants import *
from .termmap import generate_rml_termmap
import rdflib


## Adds a subject or set of subjects to the given TriplesMap
def add_subject(data, mapping, mapping_format):
    rml_subjects = []
    only_one = False

    if YARRRML_SHORTCUT_SUBJECTS in data.get(YARRRML_MAPPINGS).get(mapping):
        subject = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_SHORTCUT_SUBJECTS)
    elif YARRRML_SUBJECTS in data.get(YARRRML_MAPPINGS).get(mapping):
        subject = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_SUBJECTS)
    elif YARRRML_SUBJECT in data.get(YARRRML_MAPPINGS).get(mapping):
        subject = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_SUBJECT)
        only_one = True
    else:
        raise Exception("ERROR: no subjects in mapping " + mapping)

    if type(subject) == list and only_one:
        raise Exception("ERROR: Only one subject can be define using keyword 'subject'")

    if type(subject) != list:
        subject = [subject]

    for individual_subject in subject:
        if YARRRML_QUOTED in individual_subject or YARRRML_NON_ASSERTED in individual_subject:
            if YARRRML_CONDITION in individual_subject:
                from .predicateobject import ref_mapping
                if YARRRML_NON_ASSERTED in individual_subject:
                    subject_termmap = ref_mapping(data, mapping, individual_subject, YARRRML_NON_ASSERTED, STAR_QUOTED, mapping_format)
                else:
                    subject_termmap = ref_mapping(data, mapping, individual_subject, YARRRML_QUOTED, STAR_QUOTED, mapping_format)
                subject_termmap=subject_termmap.replace(R2RML_REFOBJECT_CLASS,STAR_CLASS).replace(R2RML_OBJECT,STAR_SUBJECT).replace("\t\t\t\t","\t\t\t\t\t").replace("\t\t","\t")
            else:
                subject_termmap = generate_rml_termmap(STAR_SUBJECT, STAR_CLASS, individual_subject, "\t\t")
        elif mapping_format == STAR_URI:
            subject_termmap = generate_rml_termmap(STAR_SUBJECT, R2RML_SUBJECT_CLASS, individual_subject, "\t\t")
        else:
            subject_termmap = generate_rml_termmap(R2RML_SUBJECT, R2RML_SUBJECT_CLASS, individual_subject, "\t\t", mapping_format)
        rml_subjects.append(subject_termmap)

    if YARRRML_GRAPHS in data.get(YARRRML_MAPPINGS).get(mapping):
        graphs = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_GRAPHS)
    elif YARRRML_GRAPH in data.get(YARRRML_MAPPINGS).get(mapping):
        graphs = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_GRAPH)
    elif YARRRML_SHORTCUT_GRAPH in data.get(YARRRML_MAPPINGS).get(mapping):
        graphs = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_SHORTCUT_GRAPH)
    else:
        graphs = []

    if type(graphs) != list:
        graphs = [graphs]

    for graph in graphs:
        graph_termmap = generate_rml_termmap(R2RML_GRAPH, R2RML_GRAPH_CLASS, graph, "\t\t\t")
        rml_subjects = list(map(lambda subject: subject[0:-4] + graph_termmap + "\t];\n", rml_subjects))

    return rml_subjects


def add_inverse_subject(tm, rdf_mapping):
    query = f'SELECT ?subject_value  WHERE {{ <{tm}> {R2RML_SUBJECT} ?subject . ' \
            f'?subject {R2RML_TEMPLATE}|{R2RML_COLUMN}|{RML_REFERENCE}|{R2RML_CONSTANT} ?subject_value' \
            f'}} '

    subject = [tm[rdflib.Variable('subject_value')].value for tm in rdf_mapping.query(query).bindings]
    if len(subject) > 1:
        logger.error("There are more than one subject in your mapping")
        raise Exception("A mapping defines one and only one subjectMap")

    else:
        subject = subject[0]
    # this means it's a column
    if not subject.startswith("http"):
        subject = '$(' + subject + ')'
    else:
        if '{' in subject:
            subject = subject.replace('{', "$(").replace('}', ')')

    query = f'SELECT ?class_value  WHERE {{ <{tm}> {R2RML_SUBJECT} ?subject . ' \
            f'?subject {R2RML_CLASS} ?class_value }} '
    classes = [tm[rdflib.Variable('class_value')] for tm in rdf_mapping.query(query).bindings]

    return subject, classes
