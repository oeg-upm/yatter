from .constants import *
from .termmap import generate_rml_termmap


local_id = 0
def add_functions(yarrrml_data):
    functions = []
    for mapping in yarrrml_data.get(YARRRML_MAPPINGS):
        mapping_data = yarrrml_data.get(YARRRML_MAPPINGS).get(mapping)
        add_internal_function(mapping, mapping_data, functions)
    return functions

def add_internal_function(mapping_id, mapping_data, functions):
    global local_id
    keys = mapping_data.keys()
    for key in keys:
        if type(mapping_data[key]) is list:
            for i in range(len(mapping_data[key])):
                value = mapping_data[key][i]
                if YARRRML_FUNCTION in value and value[YARRRML_FUNCTION] != "equal":
                    function_id = "function_" + mapping_id
                    old_id = function_id + "_"+ str(local_id)
                    function = generate_function(value, function_id)
                    functions.append(function)
                    mapping_data[key][i][YARRRML_FUNCTION] = old_id
                    local_id += 1 #different functions in the same TM
                else:
                    if type(value) is list:
                        for v in value:
                            if type(v) is dict:
                                add_internal_function(mapping_id, v, functions)
                    elif type(value) is dict:
                        add_internal_function(mapping_id, value, functions)
        elif type(mapping_data[key]) is dict and YARRRML_FUNCTION in mapping_data[key]:
            function_id = "function_" + mapping_id
            old_id = function_id + "_" + str(local_id)
            function = generate_function(mapping_data[key], function_id)
            functions.append(function)
            mapping_data[key][YARRRML_FUNCTION] = old_id
            local_id += 1  # different functions in the same TM

def generate_function(function_yarrrml_data, id_function):
    global local_id
    function = function_yarrrml_data[YARRRML_FUNCTION]
    if YARRRML_PARAMETERS in function_yarrrml_data:
        rml_function = ["<" + id_function +"_"+str(local_id)+"> a " + RML_EXECUTION_CLASS + ";\n\t"+RML_FUNCTION+" "+function+" ; \n"]
    else:
        function_yarrrml_data, function_name = split_in_line_function(function)
        rml_function = ["<" + id_function + "_" + str(
            local_id) + "> a " + RML_EXECUTION_CLASS + ";\n\t" + RML_FUNCTION + " " + function_name + " ; \n"]

    new_function = None
    if YARRRML_PARAMETERS in function_yarrrml_data:
        rml_function.append("\t"+RML_INPUT+"\n")
        parameters = function_yarrrml_data[YARRRML_PARAMETERS]
        for param in parameters:
            rml_function.append("\t\t[\n\t\t\ta "+RML_INPUT_CLASS + ";\n")
            if type(param) is list:
                param_extended = {YARRRML_PARAMETER: param[0], YARRRML_VALUE: param[1]}
            else:
                param_extended = param

            rml_function.append("\t\t\t"+RML_PARAMETER+" "+param_extended[YARRRML_PARAMETER] + ";\n")

            if YARRRML_VALUE in param_extended:
                if YARRRML_FUNCTION in param_extended[YARRRML_VALUE]:
                    local_id += 1  # new function definition within another functon
                    rml_function.append("\t\t\t" + RML_VALUE_MAP + "[\n\t\t\t\t" + RML_EXECUTION + " <"+id_function+"_"+str(local_id) +">;\n\t\t\t];\n")
                    new_function = generate_function(param_extended[YARRRML_VALUE],id_function)
                else:
                    rml_function.append(generate_rml_termmap(RML_VALUE_MAP, RML_VALUE_MAP_CLASS, param_extended[YARRRML_VALUE], "\t\t\t\t"))

            rml_function.append("\t\t],\n")


    final_function = "".join(rml_function)[0:-2]+".\n\n"
    if new_function:
        final_function += new_function

    return final_function



def split_in_line_function(function_in_line):
    parameters = {'parameters':[]}
    function_name = function_in_line.split("(")[0]
    function_in_line=function_in_line.replace(function_name, "").replace("(","",1).rsplit(")",1)[0]
    in_line_params = function_in_line.split(",")

    for param in in_line_params:
        extended_param = {}
        param_values = param.split("=",1)
        extended_param[YARRRML_PARAMETER] = param_values[0].strip()
        param_value = param_values[1].strip()

        if param_value.startswith("$("):
            extended_param[YARRRML_VALUE] = param_value
        else:
            value, internal_function_name = split_in_line_function(param_value)
            extended_param[YARRRML_VALUE] = {YARRRML_FUNCTION: internal_function_name, YARRRML_PARAMETERS: value[YARRRML_PARAMETERS]}

        parameters[YARRRML_PARAMETERS].append(extended_param)


    return parameters,function_name