from .constants import *
from .termmap import generate_rml_termmap


## Adds a subject or set of subjects to the given TriplesMap
def add_subject(data, mapping):
    subjects = []
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

    if type(subject) != list:
        subjects.append(subject)
    elif type(subject) == list and only_one:
        raise Exception("ERROR: Only one subject can be define using keyword 'subject'")
    else:
        rml_subjects = subject

    for subject in subjects:
        subject_termmap = generate_rml_termmap(R2RML_SUBJECT_PROPERTY, R2RML_SUBJECT_CLASS, subject, "\t\t")
        rml_subjects.append(subject_termmap)

    return rml_subjects
