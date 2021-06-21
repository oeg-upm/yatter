import constants


def get_initial_sources(data):
    list_initial_sources = []
    if constants.YARRRML_SOURCES in data:
        for y in data.get(constants.YARRRML_SOURCES):
            list_initial_sources.append(y)
    return list_initial_sources


def add_source(data, mapping, list_initial_sources):
    final_list = []

    if constants.YARRRML_SOURCES in data.get(constants.YARRRML_MAPPINGS).get(mapping):
        sources = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SOURCES)
    elif constants.YARRRML_SOURCE in data.get(constants.YARRRML_MAPPINGS).get(mapping):
        sources = data.get(constants.YARRRML_MAPPINGS).get(mapping).get(constants.YARRRML_SOURCE)
    else:
        raise Exception("ERROR: sources not defined in mapping " + mapping)

    if type(sources) is str:  # una unica source
        final_list.append(add_initial_source(data, sources, mapping))
    else:
        for source in sources:  # varias sources
            if source in list_initial_sources:
                final_list.append(add_initial_source(data, source, mapping))
            elif "access" in source:
                final_list.append(addSourceFull(data, mapping, source))
            elif type(source) is list: #cuidado con esto
                final_list.append(addSourceSimplified(data, mapping, source))
            else:
                raise Exception("ERROR: source " + source + " in mapping " + mapping + " not valid")
    return final_list


def add_initial_source(data, sources, mapping):
    if type(data.get("sources").get(sources)) is list:
        return addSourceSimplified(data, mapping, data.get("sources").get(sources))
    else:
        return addSourceFull(data, mapping, data.get("sources").get(sources))


def addSourceSimplified(data, mapping, sources):
    source_template = "\trml:logicalSource [\n" + "\t\ta rml:logicalSource;\n" + "\t\trml:source "
    source = sources[0]
    source_aux = source.split('~')
    source_aux1 = source_aux[0].split('.')
    source_name = source_aux1[0]
    source_extension = source_aux1[1]
    source_referenceFormulation = source_aux[1]
    if (checkExtension(source_extension, source_referenceFormulation) == 1):
        raise Exception(
            "ERROR: mismatch extension and referenceFormulation in source " + sources + " in mapping " + mapping)
    else:
        if len(sources) == 1:
            if (source_extension == "csv" or source_extension == "SQL2008"):
                source_template += '"' + source_aux[
                    0] + '"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + "\n" + "\t];\n"
            else:
                raise Exception("ERROR: source " + sources + " in mapping " + mapping + " has no iterator")
        else:
            source_delim = sources[1]
            source_template += '"' + source_aux[
                0] + '"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + ";\n" + '\t\trml:iterator "' + source_delim + '"' + ";\n\t];\n"
    return source_template


def addSourceFull(data, mapping, sour):
    source_final = ""
    if "query" in sour:
        list_source = databaseSource(data, mapping, sour)
        return list_source
    list_sources = []
    list_sources.append("sources")
    list_sources.append(data.get("mappings").get(mapping).get("sources"))
    source_template = "\trml:logicalSource [\n" + "\t\ta rml:logicalSource;\n" + "\t\trml:source "
    if "access" in sour:
        source = str(sour.get("access"))
        extension = source.split(".")
    else:
        raise Exception('ERROR: source' + sour.get("access") + 'in mapping ' + mapping + ' has no "access"')

    if "referenceFormulation" in sour:
        source_referenceFormulation = str(sour.get("referenceFormulation"))
        if checkExtension(extension[1], source_referenceFormulation) == 1:
            raise Exception("ERROR: mismatch extension and referenceFormulation in source " + sour.get(
                "access") + "in mapping " + mapping)
        if getReferenceFOrmulation(source_referenceFormulation) != "ERROR":
            source_referenceFormulation = getReferenceFOrmulation(source_referenceFormulation)
    else:
        if extension[1] == "csv":
            if "iterator" in sour:
                source_iterator = str(sour.get("iterator"))
                source_template += '"' + source + '"' + ";\n" + '\t\trml:iterator "' + source_iterator + '"\n\t];\n'
                return source_template
            else:
                source_template += '"' + source + '"' + ";\n" + '"\n\t];\n'
                return source_template
        else:
            raise Exception(
                "ERROR: source " + sour.get("access") + "in mapping " + mapping + " has no referenceFormulation")
    if "iterator" in sour:
        source_iterator = str(sour.get("iterator"))
        source_template += '"' + source + '"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + ";\n" + '\t\trml:iterator "' + source_iterator + '"\n\t];\n'
    else:
        if extension[1] == "csv" or extension[1] == "SQL2008":
            source_template += '"' + source + '"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + ";\n" + '"\n\t];\n'
        else:
            raise Exception("ERROR: source " + sour.get("access") + " in mapping " + mapping + " has no iterator")
    source_final += source_template
    return source_final


def checkExtension(extension, referenceFormulation):
    switcher = {
        "json": "jsonpath",
        "csv": "csv",
        "xml": "xpath"
        # para querys
    }
    reference = switcher.get(extension, "ERROR")
    if reference == referenceFormulation:
        return 0
    else:
        return 1


def getReferenceFOrmulation(referenceFormulation):
    switcher = {
        "jsonpath": "JSONPath",
        "csv": "CSV",
        "xpath": "XPath"
    }
    return switcher.get(referenceFormulation, "ERROR")


def databaseSource(data, mapping, source):
    list = []
    templatelog = "\trml:logicalSource [\n\t\ta rml:LogicalSource;\n"
    if "access" in source:
        if "credentials" in source:
            if "type" in source and source.get("type") == "mysql":
                templatelog += '\t\trml:source <#DataSource_' + mapping + '>;\n\t\trr:sqlVersion rr:SQL2008;\n\t\trml:query "' + source.get(
                    "query") + '";\n\t\t'
                if "referenceFormulation" in source:
                    formu = getReferenceFOrmulation(source.get("referenceFormulation"))
                    templatelog += "\t\trml:referenceFormulation ql:" + formu + "\n\t];\n"
                else:
                    templatelog += "\n\t];\n"

        else:
            raise Exception("ERROR: no credentials to get access to source in mapping " + mapping)
    else:
        raise Exception("ERROR: no access to the source in mapping " + mapping)

    list.append(templatelog)

    templateDat = '<#DataSource_' + mapping + '> a d2rq:Database;\n\tdrr1:jdbcDSN "' + source.get(
        "access") + '";\n\td2rq:jdbcDriver "com.mysql.jdbc.Driver";\n\td2rq:username "' + source.get("credentials").get(
        "username") + '";\n\td2rq:password "' + source.get("credentials").get("password") + '".\n\n'

    list.append(templateDat)

    return list
