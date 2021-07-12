import re
import constants


def get_initial_sources(data):
    list_initial_sources = []
    if constants.YARRRML_SOURCES in data:
        for y in data.get(constants.YARRRML_SOURCES):
            list_initial_sources.append(y)
    return list_initial_sources


def add_source(data, mapping, list_initial_sources):
    source_template = "\t" + constants.RML_LOGICAL_SOURCE + " [\n\t\ta " + constants.RML_LOGICAL_SOURCE_CLASS + \
                      ";\n\t\t" + constants.RML_SOURCE + " "
    final_list = []

    if constants.YARRRML_SOURCES in data.get(constants.YARRRML_MAPPINGS).get(mapping):
        sources = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SOURCES)
    elif constants.YARRRML_SOURCE in data.get(constants.YARRRML_MAPPINGS).get(mapping):  # don't find this exist
        sources = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SOURCE)
    else:
        raise Exception("ERROR: sources not defined in mapping " + mapping)

    for source in sources:
        if source in list_initial_sources:
            source = data.get(constants.YARRRML_SOURCES).get(source)

        if constants.YARRRML_ACCESS in source:
            if constants.YARRRML_QUERY in source:
                final_list.extend(source_template + database_source(mapping, source))
            else:
                final_list.append(source_template + add_source_full(mapping, source))
        elif type(source) is list:
            final_list.append(source_template + add_source_simplified(mapping, source))
        else:
            raise Exception("ERROR: source " + source + " in mapping " + mapping + " not valid")
    return final_list


def add_source_simplified(mapping, source):
    source_rdf = ""
    file_path = re.sub("~.*", "", source[0])
    reference_formulation = source[0].split('~')[1]
    source_extension = file_path.split('.')[1]
    ref_formulation_rml = reference_formulation.replace("json", "JSON").replace("csv", "CSV").replace("xpath", "XPath")
    if switch_in_reference_formulation(reference_formulation) != source_extension:
        raise Exception(
            "ERROR: mismatch extension and referenceFormulation in source " + source + " in mapping " + mapping)
    else:
        if len(source) == 1:  # si no tiene iterador
            if source_extension == "csv" or source_extension == "SQL2008":
                source_rdf += '"' + file_path + '"' + ";\n" + "\t\t" + constants.RML_REFERENCE_FORMULATION + " ql:" \
                              + ref_formulation_rml + "\n" + "\t];\n"
            else:
                raise Exception("ERROR: source " + source + " in mapping " + mapping + " has no iterator")
        else:  # source[1] es el iterador en json y xml
            source_rdf += "\"" + file_path + "\";\n\t\t" + constants.RML_REFERENCE_FORMULATION + " ql:" \
                          + ref_formulation_rml + ";\n\t\t" + constants.RML_ITERATOR + " \"" \
                          + source[1] + "\";\n\t];\n"
    return source_rdf


def add_source_full(mapping, source):
    source_rdf = ""

    access = str(source.get(constants.YARRRML_ACCESS))
    extension = access.split(".")[1]

    if constants.YARRRML_REFERENCE_FORMULATION in source:
        reference_formulation = str(source.get(constants.YARRRML_REFERENCE_FORMULATION))
        format_from_reference = switch_in_reference_formulation(reference_formulation.lower())
        ref_formulation_rml = reference_formulation.replace("json", "JSON").replace("csv", "CSV").replace("xpath","XPath")
        if extension != format_from_reference or format_from_reference == "ERROR":
            raise Exception("ERROR: not referenceFormulation found or mismatch between the format and "
                            "referenceFormulation in source " + access + "in mapping " + mapping)
        if constants.YARRRML_ITERATOR in source:
            source_iterator = str(source.get(constants.YARRRML_ITERATOR))

            source_rdf += "\"" + access + "\";\n\t\t" + constants.RML_REFERENCE_FORMULATION + " ql:" \
                          + ref_formulation_rml + ";\n\t\t" + constants.RML_ITERATOR + " \"" \
                          + source_iterator + "\"\n\t];\n"
        else:
            if extension == "csv" or extension == "SQL2008":
                source_rdf += "\"" + access + "\";\n\t\t" + constants.RML_REFERENCE_FORMULATION + " ql:" \
                              + ref_formulation_rml + ";\n\n\t];\n"
            else:
                raise Exception("ERROR: source " + access + "in mapping " + mapping + " has no referenceFormulation")

    else:
        if extension == "csv":
            source_rdf += "\"" + access + "\";\n\n\t];\n"
        else:
            raise Exception("ERROR: source " + access + "in mapping " + mapping + " has no referenceFormulation")

    return source_rdf


def database_source(mapping, source):
    source_database = []
    source_rdf = ""
    if constants.YARRRML_ACCESS in source:
        if constants.YARRRML_CREDENTIALS in source:
            if constants.YARRRML_TYPE in source:
                source_rdf += "<#DataSource_" + mapping + ">;\n\t\t" \
                              + constants.R2RML_SQL_VERSION + " rr:SQL2008;\n\t\t" \
                              + constants.R2RML_SQL_QUERY + " \"" + source.get(constants.YARRRML_QUERY) + "\";\n\t\t"
                if constants.YARRRML_REFERENCE_FORMULATION in source:
                    source_rdf += "\t\t" + constants.RML_REFERENCE_FORMULATION + " ql:" \
                                  + switch_in_reference_formulation(
                                    source.get(constants.YARRRML_REFERENCE_FORMULATION)) + "\n\t];\n"
                else:
                    source_rdf += "\n\t];\n"
                source_database.append(source_rdf)
                source_database.append(generate_database_connection(mapping, source))

        else:
            raise Exception("ERROR: no credentials to get access to source in mapping " + mapping)
    else:
        raise Exception("ERROR: no access to the source in mapping " + mapping)

    return source_database


def switch_in_reference_formulation(value):
    value = value.lower()
    if value == "csv":
        switcher = value
    elif "json" in value:
        if "path" in value:
            switcher = "json"
        else:
            switcher = "jsonpath"
    elif "x" in value:
        if "path" in value:
            switcher = "xml"
        else:
            switcher = "xpath"
    return switcher


def generate_database_connection(mapping, source):
    type = source.get(constants.YARRRML_TYPE)
    if type == "mysql":
        driver = "com.mysql.jdbc.Driver"
    elif type == "postgresql":
        driver = "org.postgresql.Driver"
    elif type == "sqlserver":
        driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    else:
        driver = ""

    database = "<#DataSource_" + mapping + "> a " + constants.D2RQ_DATABASE_CLASS + ";\n\t" \
               + constants.D2RQ_DSN + " \"" + source.get(constants.YARRRML_ACCESS) + "\";\n\t" \
               + constants.D2RQ_DRIVER + " \"" + driver + "\";\n\t" \
               + constants.D2RQ_USER + " \"" + source.get(constants.YARRRML_CREDENTIALS).get(constants.YARRRML_USERNAME) + "\";\n\t" \
               + constants.D2RQ_PASS + " \"" + source.get(constants.YARRRML_CREDENTIALS).get(constants.YARRRML_PASSWORD) + "\".\n\n"
    return database
