import pretty-yarrrml2rml.constants as constants
import pretty-yarrrml2rml.source as source
import pretty-yarrrml2rml.subject as subject
import pretty-yarrrml2rml.termmap as termmap



def get_object_access(predicate_object_map):
    if constants.YARRRML_OBJECT in predicate_object_map:
        object_access = constants.YARRRML_OBJECT
    elif constants.YARRRML_SHORTCUT_OBJECT in predicate_object_map:
        object_access = constants.YARRRML_SHORTCUT_OBJECT
    else:
        raise Exception("There isn't an object key correctly specify in " + predicate_object_map)
    return object_access


def get_predicate_access(predicate_object_map):
    if constants.YARRRML_PREDICATES in predicate_object_map:
        predicate_access = constants.YARRRML_PREDICATES
    elif constants.YARRRML_SHORTCUT_PREDICATES in predicate_object_map:
        predicate_access = constants.YARRRML_SHORTCUT_PREDICATES
    else:
        raise Exception("There isn't a predicate key correctly specify in " + predicate_object_map)
    return predicate_access


def get_predicate_object_access(mapping):
    if constants.YARRRML_PREDICATEOBJECT in mapping:
        predicate_object_access = constants.YARRRML_PREDICATEOBJECT
    elif constants.YARRRML_SHORTCUT_PREDICATEOBJECT in mapping:
        predicate_object_access = constants.YARRRML_SHORTCUT_PREDICATEOBJECT
    else:
        raise Exception("There isn't a predicate_object_map key correctly specify in " + mapping)
    return predicate_object_access


def add_predicate_object_maps(data, mapping):
    po_template = ""
    pom_text = "\t" + constants.R2RML_PREDICATE_OBJECT_MAP + " [\n"
    mapping_data = data.get(constants.YARRRML_MAPPINGS).get(mapping)
    for predicate_object_map in mapping_data.get(get_predicate_object_access(mapping_data)):
        if type(predicate_object_map) is list:
            po_template += pom_text + add_predicate_object(data, mapping, predicate_object_map) + "\n"
        else:
            po_template += pom_text + add_predicate_object(data, mapping, predicate_object_map,
                                                           get_predicate_access(predicate_object_map),
                                                           get_object_access(predicate_object_map)) + "\n"
    return po_template


def get_object_list(predicate_object, object_access):
    object_list = []
    if object_access is not None:
        object_maps = predicate_object.get(object_access)
    else:
        object_maps = predicate_object[1]

    if type(object_maps) == list:
        if len(predicate_object) == 3:
            for i in range(len(object_maps)):
                object_list.append([object_maps[i], predicate_object[2]])
        else:
            object_list.extend(object_maps)
    else:
        if len(predicate_object) == 3:
            object_list.append([object_maps, predicate_object[2]])
        else:
            object_list.append(object_maps)
    return object_list


def get_predicate_list(predicate_object, predicate_access):
    predicate_list = []
    if predicate_access is not None:
        predicate_maps = predicate_object.get(predicate_access)
    else:
        predicate_maps = predicate_object[0]
    if type(predicate_maps) == list:
        predicate_list.extend(predicate_maps)
    else:
        predicate_list.append(predicate_maps)
    return predicate_list


def add_predicate_object(data, mapping, predicate_object, predicate_access=None, object_access=None):
    template = ""
    predicate_list = get_predicate_list(predicate_object, predicate_access)
    object_list = get_object_list(predicate_object, object_access)

    for pm in predicate_list:
        template += termmap.generate_rml_termmap(constants.R2RML_PREDICATE, constants.R2RML_PREDICATE_CLASS, pm,
                                                 "\t\t\t")
    for om in object_list:
        iri = False
        if type(om) == list:
            object_value = om[0]
            if constants.YARRRML_IRI in om[0]:
                object_value = om[0].split(constants.YARRRML_IRI)[0]
                iri = True
            template += termmap.generate_rml_termmap(constants.R2RML_OBJECT, constants.R2RML_OBJECT_CLASS,
                                                     object_value, "\t\t\t")
            if len(om) == 2:
                types = termmap.check_type(om[1])
                if types != "error":
                    if types == constants.YARRRML_LANGUAGE:
                        template = template[0:len(template) - 5] + "\t\t\t" + constants.R2RML_LANGUAGE + " " \
                                   + om[1].replace(constants.YARRRML_LANG, "") + "\"\n\t\t];\n"
                    elif types == constants.YARRRML_DATATYPE:
                        template = template[0:len(template) - 5] + "\t\t\t" + constants.R2RML_DATATYPE + " " \
                                   + om[1] + "\n\t\t];\n"
            if iri:
                template = template[0:len(template) - 5] + "\t\t\t" + constants.R2RML_TERMTYPE + " " \
                           + constants.R2RML_IRI + "\n\t\t];\n"
        elif constants.YARRRML_MAPPING in om:
            template += join_mapping(data, mapping, om)
        else:
            if constants.YARRRML_VALUE in om:
                object_value = om.get(constants.YARRRML_VALUE)
            else:
                object_value = om
                if constants.YARRRML_IRI in om:
                    object_value = om.split(constants.YARRRML_IRI)[0]
                    iri = True
            template += termmap.generate_rml_termmap(constants.R2RML_OBJECT, constants.R2RML_OBJECT_CLASS,
                                                     object_value, "\t\t\t")
            if type(om) == list and constants.YARRRML_DATATYPE in om:
                template = template[0:len(template) - 5] + "\t\t\t" + constants.R2RML_DATATYPE + " " \
                           + om.get(constants.YARRRML_DATATYPE) + "\n\t\t];\n"
            if (type(om) == list and constants.YARRRML_TYPE in om and om.get(constants.YARRRML_TYPE) == "iri") or iri:
                template = template[0:len(template) - 5] + "\t\t\t" + constants.R2RML_TERMTYPE + " " \
                           + constants.R2RML_IRI + "\n\t\t];\n"
            if type(om) == list and constants.YARRRML_LANGUAGE in om:
                template = template[0:len(template) - 5] + "\t\t\t" + constants.R2RML_LANGUAGE + " \"" \
                           + om.get(constants.YARRRML_LANGUAGE) + "\"\n\t\t];\n"

    return template + "\t];"


def join_mapping(data, mapping, om):
    list_mappings = []
    template = ""
    for mappings in data.get(constants.YARRRML_MAPPINGS):
        list_mappings.append(mappings)

    mapping_join = om.get(constants.YARRRML_MAPPING)

    if mapping_join in list_mappings:
        subject_list = subject.add_subject(data, mapping_join)
        list_initial_sources = source.get_initial_sources(data)
        source_list = source.add_source(data, mapping_join, list_initial_sources)

        number_joins_rml = len(subject_list) * len(source_list)
        for i in range(number_joins_rml):
            template += "\t\t" + constants.R2RML_OBJECT + \
                        " [ \n\t\t\ta " + constants.R2RML_REFOBJECT_CLASS + \
                        ";\n\t\t\t" + constants.R2RML_PARENT_TRIPLESMAP + " <#" + mapping_join + "_" + str(i) + ">;\n"
            if constants.YARRRML_CONDITION in om:
                if constants.YARRRML_PARAMETERS in om.get(constants.YARRRML_CONDITION):
                    list_parameters = om.get(constants.YARRRML_CONDITION).get(constants.YARRRML_PARAMETERS)
                    if len(list_parameters) == 2:
                        child = list_parameters[0][1]
                        parent = list_parameters[1][1]
                        child = child.replace("$(", '"')
                        child = child.replace(")", '"')
                        parent = parent.replace("$(", '"')
                        parent = parent.replace(")", '"')

                        template += "\t\t\t" + constants.R2RML_JOIN_CONITION + \
                                    " [\n\t\t\t\t" + constants.R2RML_CHILD + " " + child + \
                                    ";\n\t\t\t\t" + constants.R2RML_PARENT + " " + parent + ";\n\t\t\t]; \n\t\t];\n"

                    else:
                        raise Exception("Error: more than two parameters in join condition in mapping1 " + mapping)
            else:
                template += "\n\t\t]\n"

    else:
        raise Exception("Error in reference mapping another mapping in mapping " + mapping)

    return template
