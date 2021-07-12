import constants


def add_mapping(mapping, it):
    map_template = "<#" + mapping + "_" + str(it) + "> a " + constants.RML_TRIPLES_MAP + ";\n\n"
    return map_template


def add_prefix(data):
    template = ""
    common_prefixes = []
    if constants.YARRRML_PREFIXES in data:
        prefixes = data.get(constants.YARRRML_PREFIXES)
        for prefix in prefixes:
            prefix_uri = data.get(constants.YARRRML_PREFIXES).get(prefix)
            check_common_prefixes(prefix_uri, common_prefixes)
            template += constants.RML_PREFIX + " " + prefix + ": <" + prefix_uri + ">.\n"

        if "r2rml" not in common_prefixes:
            template += constants.RML_PREFIX + " rr: <" + constants.R2RML_URI + ">.\n"
        if "rml" not in common_prefixes:
            template += constants.RML_PREFIX + " rml: <" + constants.RML_URI + ">.\n"
        if "rdf" not in common_prefixes:
            template += constants.RML_PREFIX + " rdf: <" + constants.RDF_URI + ">.\n"
        if "ql" not in common_prefixes:
            template += constants.RML_PREFIX + " ql: <" + constants.QL_URI + ">.\n"
        if "d2rq" not in common_prefixes:
            template += constants.RML_PREFIX + " d2rq: <" + constants.D2RQ_URI + ">.\n"
        if "base" not in common_prefixes:
            template += constants.RML_BASE + " <" + constants.EXAMPLE_URI + ">.\n"
        template += "\n\n"

    return template


def check_common_prefixes(prefix_uri, common_prefixes):

    if prefix_uri == constants.R2RML_URI:
        common_prefixes.append("r2rml")
    elif prefix_uri == constants.RML_URI:
        common_prefixes.append("rml")
    elif prefix_uri == constants.RDF_URI:
        common_prefixes.append("rdf")
    elif prefix_uri == constants.QL_URI:
        common_prefixes.append("ql")
    elif prefix_uri == constants.D2RQ_URI:
        common_prefixes.append("d2rq")
