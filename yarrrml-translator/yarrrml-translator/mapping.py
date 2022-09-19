from .import *


def add_mapping(mapping, it):
    map_template = "<#" + mapping + "_" + str(it) + "> a " + RML_TRIPLES_MAP + ";\n\n"
    return map_template


def add_prefix(data):
    template = []
    common_prefixes = []
    if YARRRML_PREFIXES in data:
        prefixes = data.get(YARRRML_PREFIXES)
        for prefix in prefixes:
            prefix_uri = data.get(YARRRML_PREFIXES).get(prefix)
            check_common_prefixes(prefix_uri, common_prefixes)
            template.append(RML_PREFIX + " " + prefix + ": <" + prefix_uri + ">.\n")

    if "r2rml" not in common_prefixes:
        template.append(RML_PREFIX + " rr: <" + R2RML_URI + ">.\n")
    if "rml" not in common_prefixes:
        template.append(RML_PREFIX + " rml: <" + RML_URI + ">.\n")
    if "rdf" not in common_prefixes:
        template.append(RML_PREFIX + " rdf: <" + RDF_URI + ">.\n")
    if "rdfs" not in common_prefixes:
        template.append(RML_PREFIX + " rdfs: <" + RDFS_URI + ">.\n")
    if "xsd" not in common_prefixes:
        template.append(RML_PREFIX + " xsd: <" + XSD_URI + ">.\n")
    if "ql" not in common_prefixes:
        template.append(RML_PREFIX + " ql: <" + QL_URI + ">.\n")
    if "d2rq" not in common_prefixes:
        template.append(RML_PREFIX + " d2rq: <" + D2RQ_URI + ">.\n")
    if "base" not in common_prefixes:
        template.append(RML_BASE + " <" + EXAMPLE_URI + ">.\n")
    template.append("\n\n")

    return "".join(template)


def check_common_prefixes(prefix_uri, common_prefixes):

    if prefix_uri == R2RML_URI:
        common_prefixes.append("r2rml")
    elif prefix_uri == RML_URI:
        common_prefixes.append("rml")
    elif prefix_uri == RDF_URI:
        common_prefixes.append("rdf")
    elif prefix_uri == QL_URI:
        common_prefixes.append("ql")
    elif prefix_uri == D2RQ_URI:
        common_prefixes.append("d2rq")
    elif prefix_uri == RDFS_URI:
        common_prefixes.append("rdfs")
    elif prefix_uri == XSD_URI:
        common_prefixes.append("xsd")
