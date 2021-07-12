import sys

import constants
import termmap


## Adds a subject or set of subjects to the given TriplesMap
def add_subject(data, mapping):
    subjects = []
    rml_subjects = []
    only_one = False

    if constants.YARRRML_SHORTCUT_SUBJECTS in data.get(constants.YARRRML_MAPPINGS).get(mapping):
        subject = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SHORTCUT_SUBJECTS)
    elif constants.YARRRML_SUBJECTS in data.get(constants.YARRRML_MAPPINGS).get(mapping):
        subject = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SUBJECTS)
    elif constants.YARRRML_SUBJECT in data.get(constants.YARRRML_MAPPINGS).get(mapping):
        subject = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SUBJECT)
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
        subject_termmap = termmap.generate_rml_termmap(constants.R2RML_SUBJECT_PROPERTY, constants.R2RML_SUBJECT_CLASS, subject, "\t\t")
        rml_subjects.append(subject_termmap)

    return rml_subjects






