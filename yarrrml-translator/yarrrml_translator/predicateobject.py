from . import *
from .source import get_initial_sources, add_source
from .subject import add_subject
from .termmap import generate_rml_termmap, check_type


def get_object_access(predicate_object_map):
    if YARRRML_OBJECT in predicate_object_map:
        object_access = YARRRML_OBJECT
    elif YARRRML_SHORTCUT_OBJECT in predicate_object_map:
        object_access = YARRRML_SHORTCUT_OBJECT
    else:
        raise Exception("There isn't an object key correctly specify in " + predicate_object_map)
    return object_access


def get_predicate_access(predicate_object_map):
    if YARRRML_PREDICATES in predicate_object_map:
        predicate_access = YARRRML_PREDICATES
    elif YARRRML_SHORTCUT_PREDICATES in predicate_object_map:
        predicate_access = YARRRML_SHORTCUT_PREDICATES
    else:
        raise Exception("There isn't a predicate key correctly specify in " + predicate_object_map)
    return predicate_access


def get_predicate_object_access(predicate_object_map):
    if YARRRML_PREDICATEOBJECT in predicate_object_map:
        predicate_object_access = YARRRML_PREDICATEOBJECT
    elif YARRRML_SHORTCUT_PREDICATEOBJECT in predicate_object_map:
        predicate_object_access = YARRRML_SHORTCUT_PREDICATEOBJECT
    else:
        raise Exception("There isn't a predicate_object_map key correctly specify in " + predicate_object_map)
    return predicate_object_access


def get_graph_access(predicate_object_map):
    if YARRRML_GRAPHS in predicate_object_map:
        graph_access = YARRRML_GRAPHS
    elif YARRRML_GRAPH in predicate_object_map:
        graph_access = YARRRML_GRAPH
    elif YARRRML_SHORTCUT_GRAPH in predicate_object_map:
        graph_access = YARRRML_SHORTCUT_GRAPH
    else:
        graph_access = None
    return graph_access


def add_predicate_object_maps(data, mapping):
    po_template = ""
    pom_text = "\t" + R2RML_PREDICATE_OBJECT_MAP + " [\n"
    mapping_data = data.get(YARRRML_MAPPINGS).get(mapping)
    for predicate_object_map in mapping_data.get(get_predicate_object_access(mapping_data)):
        if type(predicate_object_map) is list:
            po_template += pom_text + add_predicate_object(data, mapping, predicate_object_map) + "\n"
        else:
            po_template += pom_text + add_predicate_object(data, mapping, predicate_object_map,
                                                           get_predicate_access(predicate_object_map),
                                                           get_object_access(predicate_object_map),
                                                           get_graph_access(predicate_object_map)) + "\n"
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
        if object_access is None and len(predicate_object) == 3:
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

def get_graph_list(predicate_object,graph_access):
    if graph_access is not None:
        graphs = predicate_object.get(graph_access)
        if type(graphs) is not list:
            graphs = [graphs]
    else:
        graphs = []
    return graphs
def add_predicate_object(data, mapping, predicate_object, predicate_access=None, object_access=None, graph_access=None):
    template = ""
    predicate_list = get_predicate_list(predicate_object, predicate_access)
    object_list = get_object_list(predicate_object, object_access)
    graph_list = get_graph_list(predicate_object, graph_access)

    for pm in predicate_list:
        template += generate_rml_termmap(R2RML_PREDICATE, R2RML_PREDICATE_CLASS, pm,
                                         "\t\t\t")
    for om in object_list:
        iri = False
        if type(om) == list:
            object_value = om[0]
            if YARRRML_IRI in om[0]:
                object_value = om[0].split(YARRRML_IRI)[0]
                iri = True
            template += generate_rml_termmap(R2RML_OBJECT, R2RML_OBJECT_CLASS,
                                             object_value, "\t\t\t")
            if len(om) == 2:
                types = check_type(om[1])
                if types != "error":
                    if types == YARRRML_LANGUAGE:
                        template = template[0:len(template) - 5] + "\t\t\t" + R2RML_LANGUAGE + " \"" \
                                   + om[1].replace(YARRRML_LANG, "") + "\"\n\t\t];\n"
                    elif types == YARRRML_DATATYPE:
                        template = template[0:len(template) - 5] + "\t\t\t" + R2RML_DATATYPE + " " \
                                   + om[1] + "\n\t\t];\n"
            if iri:
                template = template[0:len(template) - 5] + "\t\t\t" + R2RML_TERMTYPE + " " \
                           + R2RML_IRI + "\n\t\t];\n"
        elif YARRRML_MAPPING in om:
            template += join_mapping(data, mapping, om)
        else:
            if YARRRML_VALUE in om:
                object_value = om.get(YARRRML_VALUE)
            else:
                object_value = om
                if YARRRML_IRI in om:
                    object_value = om.split(YARRRML_IRI)[0]
                    iri = True
            template += generate_rml_termmap(R2RML_OBJECT, R2RML_OBJECT_CLASS,
                                             object_value, "\t\t\t")
            if type(om) == list and YARRRML_DATATYPE in om:
                template = template[0:len(template) - 5] + "\t\t\t" + R2RML_DATATYPE + " " \
                           + om.get(YARRRML_DATATYPE) + "\n\t\t];\n"
            if (type(om) == list and YARRRML_TYPE in om and om.get(YARRRML_TYPE) == "iri") or iri:
                template = template[0:len(template) - 5] + "\t\t\t" + R2RML_TERMTYPE + " " \
                           + R2RML_IRI + "\n\t\t];\n"
            if type(om) == list and YARRRML_LANGUAGE in om:
                template = template[0:len(template) - 5] + "\t\t\t" + R2RML_LANGUAGE + " \"" \
                           + om.get(YARRRML_LANGUAGE) + "\"\n\t\t];\n"


    for graph in graph_list:
        template += generate_rml_termmap(R2RML_GRAPH, R2RML_GRAPH_CLASS, graph, "\t\t\t")

    return template + "\t];"


def join_mapping(data, mapping, om):
    list_mappings = []
    template = ""
    for mappings in data.get(YARRRML_MAPPINGS):
        list_mappings.append(mappings)

    mapping_join = om.get(YARRRML_MAPPING)

    if mapping_join in list_mappings:
        subject_list = add_subject(data, mapping_join)
        list_initial_sources = get_initial_sources(data)
        source_list = add_source(data, mapping_join, list_initial_sources)

        number_joins_rml = len(subject_list) * len(source_list)
        for i in range(number_joins_rml):
            template += "\t\t" + R2RML_OBJECT + \
                        " [ \n\t\t\ta " + R2RML_REFOBJECT_CLASS + \
                        ";\n\t\t\t" + R2RML_PARENT_TRIPLESMAP + " <#" + mapping_join + "_" + str(i) + ">;\n"
            if YARRRML_CONDITION in om:
                conditions = om.get(YARRRML_CONDITION)
                if type(conditions) is not list:
                    conditions = [conditions]
                for condition in conditions:
                    if YARRRML_PARAMETERS in condition:
                        list_parameters = condition.get(YARRRML_PARAMETERS)
                        if len(list_parameters) == 2:
                            child = list_parameters[0][1].replace("$(", '"').replace(")", '"')
                            parent = list_parameters[1][1].replace("$(", '"').replace(")", '"')

                            template += "\t\t\t" + R2RML_JOIN_CONITION + \
                                        " [\n\t\t\t\t" + R2RML_CHILD + " " + child + \
                                        ";\n\t\t\t\t" + R2RML_PARENT + " " + parent + ";\n\t\t\t]; \n"

                        else:
                            raise Exception("Error: more than two parameters in join condition in mapping1 " + mapping)
                template += "\t\t];\n"
            else:
                template += "\n\t\t]\n"

    else:
        raise Exception("Error in reference mapping another mapping in mapping " + mapping)

    return template
