import re
from .constants import *


def get_initial_sources(data):
    list_initial_sources = []
    if YARRRML_SOURCES in data:
        for y in data.get(YARRRML_SOURCES):
            list_initial_sources.append(y)
    return list_initial_sources


def get_sources(data, mapping):
    if YARRRML_SOURCES in data.get(YARRRML_MAPPINGS).get(mapping):
        sources = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_SOURCES)
    elif YARRRML_SOURCE in data.get(YARRRML_MAPPINGS).get(mapping):
        sources = data.get(YARRRML_MAPPINGS).get(mapping).get(YARRRML_SOURCE)
        if type(sources) is not list:
            sources = [sources]
    else:
        raise Exception("ERROR: sources not defined in mapping " + mapping)

    return sources


def add_source(data, mapping, list_initial_sources):
    source_template = "\t" + RML_LOGICAL_SOURCE + " [\n\t\ta " + RML_LOGICAL_SOURCE_CLASS + \
                      ";\n\t\t" + RML_SOURCE + " "
    final_list = []
    sources = get_sources(data, mapping)
    for source in sources:

        if source in list_initial_sources:
            source = data.get(YARRRML_SOURCES).get(source)

        if YARRRML_ACCESS in source:
            if YARRRML_QUERY in source:
                final_list.append(source_template + database_source(mapping, source))
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
                source_rdf += '"' + file_path + '"' + ";\n" + "\t\t" + RML_REFERENCE_FORMULATION + " ql:" \
                              + ref_formulation_rml + "\n" + "\t];\n"
            else:
                raise Exception("ERROR: source " + source + " in mapping " + mapping + " has no iterator")
        else:  # source[1] es el iterador en json y xml
            source_rdf += "\"" + file_path + "\";\n\t\t" + RML_REFERENCE_FORMULATION + " ql:" \
                          + ref_formulation_rml + ";\n\t\t" + RML_ITERATOR + " \"" \
                          + source[1] + "\";\n\t];\n"
    return source_rdf


def add_source_full(mapping, source):
    source_rdf = ""

    access = str(source.get(YARRRML_ACCESS))
    extension = access.split(".")[1]

    if YARRRML_REFERENCE_FORMULATION in source:
        reference_formulation = str(source.get(YARRRML_REFERENCE_FORMULATION))
        format_from_reference = switch_in_reference_formulation(reference_formulation.lower())
        ref_formulation_rml = reference_formulation.replace("json", "JSON").replace("csv", "CSV").replace("xpath",
                                                                                                          "XPath")
        if extension != format_from_reference or format_from_reference == "ERROR":
            raise Exception("ERROR: not referenceFormulation found or mismatch between the format and "
                            "referenceFormulation in source " + access + "in mapping " + mapping)
        if YARRRML_ITERATOR in source:
            source_iterator = str(source.get(YARRRML_ITERATOR))

            source_rdf += "\"" + access + "\";\n\t\t" + RML_REFERENCE_FORMULATION + " ql:" \
                          + ref_formulation_rml + ";\n\t\t" + RML_ITERATOR + " \"" \
                          + source_iterator + "\"\n\t];\n"
        else:
            if extension == "csv" or extension == "SQL2008":
                source_rdf += "\"" + access + "\";\n\t\t" + RML_REFERENCE_FORMULATION + " ql:" \
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
    source_rdf = ""
    if YARRRML_ACCESS in source:
        if YARRRML_CREDENTIALS in source:
            if YARRRML_TYPE in source:
                type = source.get(YARRRML_TYPE)
                access = source.get(YARRRML_ACCESS)
                username = source.get(YARRRML_CREDENTIALS).get(YARRRML_USERNAME)
                password = source.get(YARRRML_CREDENTIALS).get(YARRRML_PASSWORD)
                hash_datasource = abs(hash(access + type + username + password))
                source_rdf += "<#DataSource_" + str(hash_datasource) + ">;\n\t\t" \
                              + R2RML_SQL_VERSION + " rr:SQL2008;\n\t\t" \
                              + R2RML_SQL_QUERY + " \"" + source.get(YARRRML_QUERY) + "\";\n\t\t"
                if YARRRML_REFERENCE_FORMULATION in source:
                    source_rdf += "\t\t" + RML_REFERENCE_FORMULATION + " ql:" \
                                  + switch_in_reference_formulation(
                        source.get(YARRRML_REFERENCE_FORMULATION)) + "\n\t];\n"
                else:
                    source_rdf += "\n\t];\n"
        else:
            raise Exception("ERROR: no credentials to get access to source in mapping " + mapping)
    else:
        raise Exception("ERROR: no access to the source in mapping " + mapping)

    return source_rdf


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


def generate_database_connections(data):
    database = []
    hash_ids = []
    for mapping in data.get(YARRRML_MAPPINGS):
        sources = get_sources(data, mapping)
        for source in sources:
            if YARRRML_ACCESS and YARRRML_QUERY in source:
                type = source.get(YARRRML_TYPE)
                if type == "mysql":
                    driver = "com.mysql.jdbc.Driver"
                elif type == "postgresql":
                    driver = "org.postgresql.Driver"
                elif type == "sqlserver":
                    driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
                else:
                    driver = None
                access = source.get(YARRRML_ACCESS)
                username = source.get(YARRRML_CREDENTIALS).get(YARRRML_USERNAME)
                password = source.get(YARRRML_CREDENTIALS).get(YARRRML_PASSWORD)
                hash_datasource = abs(hash(access + type + username + password))
                if not hash_datasource in hash_ids:
                    hash_ids.append(hash_datasource)
                    if driver is None:
                        database.append("<#DataSource_" + str(hash_datasource) + "> a " + D2RQ_DATABASE_CLASS + ";\n\t"
                                        + D2RQ_DSN + " \"" + access + "\";\n\t"
                                        + D2RQ_USER + " \"" + username + "\";\n\t"
                                        + D2RQ_PASS + " \"" + password + "\".\n\n")
                    else:
                        database.append("<#DataSource_" + str(hash_datasource) + "> a " + D2RQ_DATABASE_CLASS + ";\n\t"
                                        + D2RQ_DSN + " \"" + access + "\";\n\t"
                                        + D2RQ_DRIVER + " \"" + driver + "\";\n\t"
                                        + D2RQ_USER + " \"" + username + "\";\n\t"
                                        + D2RQ_PASS + " \"" + password + "\".\n\n")
    return database
