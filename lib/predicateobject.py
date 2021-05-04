import yaml

def addPredicateObject(data,mapping):
    po_template = ""
    if ("predicateobjects" in data.get("mappings").get(mapping)):
        for predob in data.get("mappings").get(mapping).get("predicateobjects"):
            if "predicates" in predob:
                #full
                po_template+=addPredicateObjectFull(data,mapping,predob,"predicates")
            #elif "predicate" in data.get("mappings").get(mapping).get("predicatesobjects")
            elif "p" in predob:
                #full con acceso a p
                po_template+=addPredicateObjectFull(data,mapping,predob,"p")
            else:
                    if type(predob) is list:
                        po_template+=addPredicateObjectSimplified(data,mapping,predob)
                    else:
                        #ERROR
                        raise Exception("Error: Incorrect predicateObject Map in mapping " + mapping)

    elif ("po" in data.get("mappings").get(mapping)):
        for predob in data.get("mappings").get(mapping).get("po"):
            if "predicates" in predob:
                #full
                po_template+=addPredicateObjectFull(data,mapping,predob,"predicates")
            #elif "predicate" in data.get("mappings").get(mapping).get("po")
            elif "p" in predob:
                #full con acceso a p
                po_template+=addPredicateObjectFull(data,mapping,predob,"p")
            else:
                if type(predob) is list:
                    po_template+=addPredicateObjectSimplified(data,mapping,predob)
                else:
                    #ERROR
                    raise Exception("Error: Incorrect predicateObject Map in mapping " + mapping)
    else:
        #¿ERROR?
        raise Exception("Error: ") #Creo que no sería necesario, que puede haber 0 predicate objects


    return po_template


def addPredicateObjectSimplified(data,mapping,predob):
    template= "\trr:predicateObjectMap [\n\t\ta rr:PredicateObjectMap;\n"
    if(type(predob[0]) == list and len(predob)==2):
        for predicate in predob[0]:
            template+="\t\trr:predicate "+str(predicate)+";\n"
        for object in predob[1]:
            template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
            object=str(object)
            object=object.replace("$(",'"')
            object=object.replace(")",'"')
            template+="\t\t\trml:reference " + object + "\n\t\t];\n"
        template = template[:-2]
        template+="\n\t];\n"

    elif(len(predob)==2):
        ##solo predicado y objeto

        template+="\t\trr:predicate "+str(predob[0])+";\n"+"\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
        object=str(predob[1])
        object=object.replace("$(",'"')
        object=object.replace(")",'"')
        template+="\t\t\trml:reference " + object + "\n\t\t]\n\t];\n\n"

    elif(len(predob)==3):
        #1 pred, 2 obj, 3 datatype, leng
        template+="\t\trr:predicate "+str(predob[0])+";\n"+"\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
        object=str(predob[1])
        object=object.replace("$(",'"')
        object=object.replace(")",'"')
        template+="\t\t\trml:reference " + object + "\n"
        types = check_type(predob,3)
        if(types!="error"):
            template+="\t\t\trr:" + types +" "+ predob[2] +"\n\t\t]\n\t];\n\n"
        else:
            raise Exception("Error: incorrect format of predicateObjectMap in mapping " + mapping)
    else:
        #ERROR
        raise Exception("Error: incorrect format of predicateObjectMap in mapping " + mapping)

    return template

def addPredicateObjectFull(data,mapping,predob,access):
    template=""
    #COMPROBAR SI ES LISTA PRIMERO
    if(type(predob.get(access))!= list):
        template="\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n\t\trr:predicate " + predob.get(access) +"\n"
        if "objects" in predob:
            if "value" in predob.get("objects"):
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=predob.get("objects").get("value")
                object=object.replace("$(",'"')
                object=object.replace(")",'"')
                template+="\t\t\trml:reference " + object + ";\n"
                "\t\t]\n\t];\n\n"
                if "datatype" in predob.get("objects"):
                    template+= "\t\t\trr:datatype " + predob.get("objects").get("datatype") + "\n\t\t]\n\t];\n\n"
                elif "type" in predob.get("objects"):
                    template+= "\t\t\trr:TermType " + predob.get("objects").get("type") + "\n\t\t]\n\t];\n\n"
                elif "language" in predob.get("objects"):
                    template+= '\t\t\trr:language "' + predob.get("objects").get("language") + '"\n\t\t]\n\t];\n\n'
            elif "mapping" in predob.get("objects"):
                template+= joinMapping(data,mapping,predob,"objects")
            else:
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=predob.get("objects")
                object=object.replace("$(",'"')
                object=object.replace(")",'"')
                template+="\t\t\trml:reference " + object + ";\n\t\t]\n\t];\n\n"
        elif "o" in predob:
            if "value" in predob.get("o"):
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=predob.get("o").get("value")
                object=object.replace("$(",'"')
                object=object.replace(")",'"')
                template+="\t\t\trml:reference " + object + ";\n"
                "\t\t]\n\t];\n\n"
                if "datatype" in predob.get("o"):
                    template+= "\t\t\trr:datatype " + predob.get("o").get("datatype") + "\n\t\t]\n\t];\n\n"
                elif "type" in predob.get("o"):
                    template+= "\t\t\trr:TermType " + predob.get("o").get("type") + "\n\t\t]\n\t];\n\n"
                elif "language" in predob.get("o"):
                    template+= '\t\t\trr:language "' + predob.get("o").get("language") + '"\n\t\t]\n\t];\n\n'
            elif "mapping" in predob.get("o"):
                template+= joinMapping(data,mapping,predob,"o")
            else:
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=predob.get("o")
                object=object.replace("$(",'"')
                object=object.replace(")",'"')
                template+="\t\t\trml:reference " + object + ";\n\t\t]\n\t];\n\n"
    else:
        if("objects" in predob):
            if len(predob.get(access)) == len(predob.get("objects")):
                template="\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n"
                for predic in predob.get(access):
                    template+= "\t\trr:predicate " + str(predic) + ";\n"
                for objec in predob.get("objects"):
                    print("THe object is "+ str(objec))
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    if(type(objec) is list):
                        object = objec[0]
                        object=object.replace("$(",'"')
                        object=object.replace(")",'"')
                    else:
                        object=objec.replace("$(",'"')
                        object=object.replace(")",'"')
                    template+="\t\t\trml:reference " + object + ";\n"
                    if type(objec)== list and len(objec)==2:
                        types = check_type(objec,2)
                        if(types!="error"):
                            if(types=="iri"):
                                template+="\t\t\trr:TermType rr:IRI"+"\n\t\t];\n"
                            elif(types=="language"):
                                lenguage=objec[1].replace("~lang","")
                                template+='\t\t\trr:language "'+  lenguage +'"\n\t\t];\n'
                            elif(types=="datatype"):
                                template+="\t\t\trr:datatype "+  objec[1] +"\n\t\t];\n"
                        else:
                            raise Exception("Error: incorrect format of predicateObjectMap in mapping " + mapping)
                    else:
                        template+="\t\t];\n"
                template=template[:-2]
                template+= "\n\t];\n\n"
            else:
                raise Exception("Error: Not the same number of predicates and objects in mapping " + mapping)

        elif ("o" in predob):
            if len(predob.get(access))== len(predob.get("o")):
                template="\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n"
                for predic in predob.get(access):
                    template+= "\t\trr:predicate " + str(predic) + ";\n"
                for objec in predob.get("objects"):
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    if(type(objec) is list):
                        object = objec[0]
                        object=object.replace("$(",'"')
                        object=object.replace(")",'"')
                    else:
                        object=objec.replace("$(",'"')
                        object=object.replace(")",'"')
                    template+="\t\t\trml:reference " + object + ";\n\t\t];\n"
                    if type(objec)== list and len(objec)==2:
                        types = check_type(objec,2)
                        if(types!="error"):
                            if(types=="iri"):
                                template+="\t\t\trr:TermType rr:IRI\n\t\t];\n"
                            elif(types=="language"):
                                lenguage=objec[1].replace("~lang","")
                                template+='\t\t\trr:language "'+  lenguage +'"\n\t\t];\n'
                            elif(types=="datatype"):
                                template+="\t\t\trr:datatype "+  objec[1] +"\n\t\t];\n"
                        else:
                            raise Exception("Error: incorrect format of predicateObjectMap in mapping " + mapping)
                template=template[:-2]
                template+= "\n\t];\n\n"
            else:
                raise Exception("Error: Not the same number of predicates and objects in mapping " + mapping)

    return template

def check_type(predob,pos):

    type=str(predob[pos-1])
    if "~iri" in type:
        return "iri"
    elif "~lang" in type:
        return "language"
    elif ("xsd:" in type) or ("ex:" in type):
        return "datatype"
    else:
        return "error"

def joinMapping(data,mapping,predob,access):
    list_mappings=[]
    for mappings in data.get("mappings"):
        list_mappings.append(mappings)

    if predob.get(access).get("mapping") in list_mappings and predob.get(access).get("mapping") != mapping:
        template="\t\trr:objectMap [ \n\t\t\ta rr:RefObjectMap;\n\t\t\trr:parentTriplesMap <#"+ predob.get(access).get("mapping") +">;\n"

        if "condition" in predob.get(access):
            if "parameters" in predob.get(access).get("condition"):
                list_parameters = predob.get(access).get("condition").get("parameters")
                if len(list_parameters)==2:
                    child=list_parameters[0][1]
                    parent=list_parameters[1][1]
                    print(child)
                    print(parent)
                    child=child.replace("$(",'"')
                    child=child.replace(")",'"')
                    parent=parent.replace("$(",'"')
                    parent=parent.replace(")",'"')

                    template+='\t\t\trr:joinCondition [\n\t\t\t\trr:child ' + child + ';\n\t\t\t\trr:parent ' + parent + ';\n\t\t\t]\n\t\t]\n\t];\n\n'

                else:
                    raise Exception("Error: more than two parameters in join condition in mapping " + mapping)
        else:
            template+="\n\t\t]\n\t];\n\n"
            return template


    else:
        raise Exception("Error in reference mapping another mapping " + mapping)
    return template
