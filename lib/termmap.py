import constants


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
def generate_rml_termmap(rml_property, rml_class, text):
    template = "\t" + rml_property + " [\n\t\ta " + rml_class + ";\n\t\t"
    term_map = get_termmap_type(text)
    if term_map == "rr:template":
        text = text.replace("$(", "{")
        text = text.replace(")", "}")
    else:
        text = text.replace("$(", "")
        text = text.replace(")", "")
    if term_map != "rr:constant":
        template += term_map + " \"" + text + "\";\n\t];\n"
    else:
        template += term_map + " " + text + ";\n\t];\n\n"

    return template


def check_type(om):
    if "~lang" in om:
        return "language"
    elif ":" in om:
        return "datatype"
    else:
        return "error"