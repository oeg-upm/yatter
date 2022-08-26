from .constants import *
from .termmap import generate_rml_termmap


## Adds a subject or set of subjects to the given TriplesMap
def add_subject(data, mapping):
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
        subject_termmap = generate_rml_termmap(R2RML_SUBJECT, R2RML_SUBJECT_CLASS, individual_subject, "\t\t")
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
        rml_subjects = list(map(lambda subject : subject[0:-4] + graph_termmap + "\t];\n", rml_subjects))




    return rml_subjects
