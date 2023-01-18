from .import *


def add_mapping(mapping, mappings, it):
    map_template = "<" + mapping + "_" + str(it) + "> a "
    if mappings[mapping]:
        if mappings[mapping] == "non_asserted":
            map_template += STAR_NON_ASSERTED_CLASS + ", "
    map_template += R2RML_TRIPLES_MAP + ";\n\n"
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
    if "foaf" not in common_prefixes:
        template.append(RML_PREFIX + " foaf: <" + FOAF_URI + ">.\n")
    if "schema" not in common_prefixes:
        template.append(RML_PREFIX + " schema: <" + SCHEMA_URI + ">.\n")
    if "formats" not in common_prefixes:
        template.append(RML_PREFIX + " formats: <" + FORMATS_URI + ">.\n")
    if "comp" not in common_prefixes:
        template.append(RML_PREFIX + " comp: <" + COMPRESSION_URI + ">.\n")
    if "void" not in common_prefixes:
        template.append(RML_PREFIX + " void: <" + VOID_URI + ">.\n")
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
    elif prefix_uri == FOAF_URI:
        common_prefixes.append("foaf")
    elif prefix_uri == SCHEMA_URI:
        common_prefixes.append("schema")
    elif prefix_uri == FORMATS_URI:
        common_prefixes.append("formats")
    elif prefix_uri == COMPRESSION_URI:
        common_prefixes.append("comp")
    elif prefix_uri == VOID_URI:
        common_prefixes.append("void")


def add_inverse_prefix(rdf_mapping):
    prefixes = {}
    for prefix, uri in rdf_mapping.namespaces():
        if prefix:
            prefixes[prefix] = uri.toPython()
    return prefixes


def get_non_asserted_mappings(yarrrml_data, mapping_format):
    mappings =  dict.fromkeys(list(yarrrml_data.get(YARRRML_MAPPINGS).keys()))
    for mapping in yarrrml_data.get(YARRRML_MAPPINGS):
        keys = yarrrml_data.get(YARRRML_MAPPINGS).get(mapping).keys()
        for key in keys:
            if type(yarrrml_data.get(YARRRML_MAPPINGS).get(mapping).get(key)) is dict:
                values = yarrrml_data.get(YARRRML_MAPPINGS).get(mapping).get(key)
                if YARRRML_NON_ASSERTED in values:
                    mappings[values[YARRRML_NON_ASSERTED]] = "non_asserted"
                    mapping_format = STAR_URI
                elif YARRRML_QUOTED in values:
                    mapping_format = STAR_URI
            if type(yarrrml_data.get(YARRRML_MAPPINGS).get(mapping).get(key)) is list and key==YARRRML_SHORTCUT_PREDICATEOBJECT:
                for value in yarrrml_data.get(YARRRML_MAPPINGS).get(mapping).get(key):
                    if type(value) is dict and YARRRML_SHORTCUT_OBJECT in value:
                        if YARRRML_NON_ASSERTED in value[YARRRML_SHORTCUT_OBJECT]:
                            mappings[value[YARRRML_SHORTCUT_OBJECT][YARRRML_NON_ASSERTED]] = "non_asserted"
                            mapping_format = STAR_URI
                        elif YARRRML_QUOTED in value[YARRRML_SHORTCUT_OBJECT]:
                            mapping_format = STAR_URI

    return mappings, mapping_format


def add_logical_targets(yarrrml_data):
    logical_targets = []
    if YARRRML_TARGETS in yarrrml_data:
        targets = yarrrml_data.get(YARRRML_TARGETS)
        keys = targets.keys()
        for key in keys:
            logical_targets.extend(generate_logical_target(targets.get(key), key))

    for mapping in yarrrml_data.get(YARRRML_MAPPINGS):
        mapping_data = yarrrml_data.get(YARRRML_MAPPINGS).get(mapping)
        add_internal_logical_target(mapping, mapping_data, logical_targets)

    return logical_targets


def add_internal_logical_target(mapping_id,mapping_data, internal_targets, local_target_id = 0):
    keys = mapping_data.keys()
    for key in keys:
        if type(mapping_data[key]) is list:
            for i in range(len(mapping_data[key])):
                value = mapping_data[key][i]
                if YARRRML_TARGETS in value:
                    target_value=value[YARRRML_TARGETS]
                    if type(target_value) is dict or type(target_value) is list:
                        logical_target_id = "logical_target_" + mapping_id+"_"+str(local_target_id)
                        internal_targets.extend(generate_logical_target(target_value, logical_target_id))
                        mapping_data[key][i][YARRRML_TARGETS] = logical_target_id
                        local_target_id += 1
                else:
                    if type(value) is list:
                        for v in value:
                            if type(v) is dict:
                                add_internal_logical_target(mapping_id, v, internal_targets, local_target_id)
                    elif type(value) is dict:
                        add_internal_logical_target(mapping_id, value, internal_targets, local_target_id)
        elif YARRRML_TARGETS in mapping_data[key]:
            target_value = mapping_data[key][YARRRML_TARGETS]
            logical_target_id = "logical_target_" + mapping_id + "_" + str(local_target_id)
            internal_targets.extend(generate_logical_target(target_value, logical_target_id))
            mapping_data[key][YARRRML_TARGETS] = logical_target_id
            local_target_id += 1

def generate_logical_target(target_yaml_data, id_target):
    logical_targets = []
    output_type = None
    format = None
    compression = None
    target_yaml_data_list = target_yaml_data
    if (type(target_yaml_data) is list and type(target_yaml_data[0]) is str) or type(target_yaml_data) is dict:
        target_yaml_data_list = [target_yaml_data]

    for target_yaml_data in target_yaml_data_list:
        logical_target = ["<" + id_target + "> a " + RML_LOGICAL_TARGET_CLASS + ";\n"]
        if type(target_yaml_data) is list:
            value = target_yaml_data[0].split("~")
            access = value[0]
            if len(value) == 2:
                output_type = value[1]
            if len(target_yaml_data) >= 2:
                format = "formats:" + YARRRML_OUTPUT_FORMAT[target_yaml_data[1]]
            if len(target_yaml_data) == 3:
                compression = "comp:" + target_yaml_data[2]
        else:
            access = target_yaml_data[YARRRML_ACCESS]
            if YARRRML_TYPE in target_yaml_data:
                output_type = target_yaml_data[YARRRML_TYPE]
            if YARRRML_SERIALIZATION in target_yaml_data:
                format = "formats:" + YARRRML_OUTPUT_FORMAT[target_yaml_data[YARRRML_SERIALIZATION]]
            if YARRRML_COMPRESSION in target_yaml_data:
                compression = "comp:" + target_yaml_data[YARRRML_COMPRESSION]

        logical_target.append("\t " + RML_TARGET + " [\n\t\t")

        if output_type == "sparql":
            logical_target.append("sd:endpoint <" + access + ">;\n\t\tsd:supportedLanguage sd:SPARQL11Update\n\t];\n")
        elif output_type == "dcat":
            logical_target.append("a dcat:Dataset;\n\t\tdcat:dataDump <" + access + ">\n\t];\n")
        else:
            logical_target.append("a void:Dataset;\n\t\tvoid:dataDump <" + access + ">\n\t];\n")

        if format:
            logical_target.append("\t " + RML_SERIALIZATION + " " + format + ";")
        else:
            logical_target.append("\t " + RML_SERIALIZATION + " formats:N-Quads;")

        if compression:
            logical_target.append("\n\t " + RML_COMPRESSION + " " + compression + ";")
        logical_targets.append("".join(logical_target)[0:-1] + ".\n\n")
    return logical_targets
def merge_mapping_section_by_key(key,yarrrml_list):
    output = {key:{}}
    for yarrrml_mapping in yarrrml_list:
        output[key] =  output[key] | yarrrml_mapping
    return output