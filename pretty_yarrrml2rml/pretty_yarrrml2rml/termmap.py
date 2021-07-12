import pretty_yarrrml2rml.constants as constants


## return the type of TermMap based on the input text
def get_termmap_type(text):
    if "$(" in text and ")" in text:
        if text[0] == "$" and text[len(text) - 1] == ")" and text.count("$(") == 1:
            return constants.RML_REFERENCE
        else:
            return constants.R2RML_TEMPLATE
    else:
        return constants.R2RML_CONSTANT


## Generates a TermMap (subject, predicate, object) based on the property, class and the text
def generate_rml_termmap(rml_property, rml_class, text, identation):
    template = identation[0:-1] + rml_property + " [\n"+identation+"a " + rml_class + ";\n" + identation
    term_map = get_termmap_type(text)
    if term_map == constants.R2RML_TEMPLATE:
        text = text.replace("$(", "{")
        text = text.replace(")", "}")
    elif term_map == constants.RML_REFERENCE:
        text = text.replace("$(", "")
        text = text.replace(")", "")
    elif term_map == constants.R2RML_CONSTANT and text == "a":
        text = constants.RDF_TYPE
    if term_map != "rr:constant":
        template += term_map + " \"" + text + "\";\n"+identation[0:-1]+"];\n"
    else:
        template += term_map + " " + text + ";\n"+identation[0:-1]+"];\n"

    return template


def check_type(om):
    if "~lang" in om:
        return "language"
    elif ":" in om:
        return "datatype"
    else:
        return "error"
