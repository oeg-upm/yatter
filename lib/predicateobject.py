import yaml
import source as sourcemod
import subject as subjectmod

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
    if((type(predob[0]) == list or type(predob[1])==list) and len(predob)==2):
        if(type(predob[0])==list):
            for predicate in predob[0]:
                template+="\t\trr:predicate "+str(predicate)+";\n"
        else:
            template+="\t\trr:predicate "+str(predob[0])+";\n"
        if(type(predob[1])==list):
            for object in predob[1]:
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=str(object)
                termMap=getTermMap(object)
                if(termMap=='rr:template "'):
                    object=object.replace("$",'')
                    object=object.replace("(","{")
                    object=object.replace(")",'}')
                else:
                    object=object.replace("$(",'')
                    object=object.replace(")",'')
                types=check_type_simple(object)
                if(types=="error"):
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n'
                else:
                    if(types=="iri"):
                        object=object.replace("~iri","")
                        template+="\t\t\t"+ termMap + object + '";\n'
                        template+="\t\t\trr:TermType rr:IRI"+"\n\t\t]\n\t];\n\n"
                    elif(types=="language"):
                        lenguage=object.replace("~lang","")
                        template+='\t\t\trr:language "'+  lenguage +'"\n\t\t]\n\t];\n\n'
                    elif(types=="datatype"):
                        template+="\t\t\trr:datatype "+  object +"\n\t\t]\n\t];\n\n"
        else:
            template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
            object=str(predob[1])
            termMap=getTermMap(object)
            if(termMap=='rr:template "'):
                object=object.replace("$",'')
                object=object.replace("(","{")
                object=object.replace(")",'}')
            else:
                object=object.replace("$(",'')
                object=object.replace(")",'')
            types=check_type_simple(object)
            if(termMap!='rr:constant '):
                template+="\t\t\t"+ termMap + object + '"'+ ';\n'
            else:
                template+="\t\t\t"+ termMap + object + ';\n'
            if(types!="error"):
                if(types=="iri"):
                    template+="\t\t\trr:TermType rr:IRI"+"\n\t\t]\n\t];\n\n"
                elif(types=="language"):
                    lenguage=object.replace("~lang","")
                    template+='\t\t\trr:language "'+  lenguage +'"\n\t\t]\n\t];\n\n'
                elif(types=="datatype"):
                    template+="\t\t\trr:datatype "+  object +"\n\t\t]\n\t];\n\n"


        template = template[:-2]
        template+="\n\t];\n"

    elif(len(predob)==2):
        ##solo predicado y objeto

        template+="\t\trr:predicate "+str(predob[0])+";\n"+"\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
        object=str(predob[1])
        if "~" in object:
            termMap=getTermMap(object)
            if(termMap=='rr:template "'):
                object=object.replace("$",'')
                object=object.replace("(","{")
                object=object.replace(")",'}')
            else:
                object=object.replace("$(",'')
                object=object.replace(")",'')
            types=check_type_simple(object)
            object1=object.split("~")
            if(termMap!='rr:constant '):
                template+="\t\t\t"+ termMap + object1[0] + '"'+ ';\n'
            else:
                template+="\t\t\t"+ termMap + object1[0] + ';\n'
            if(types!="error"):
                if(types=="iri"):
                    template+="\t\t\trr:TermType rr:IRI"+"\n\t\t]\n\t];\n\n"
                elif(types=="language"):
                    lenguage=objec[1].replace("~lang","")
                    template+='\t\t\trr:language "'+  lenguage +'"\n\t\t]\n\t];\n\n'
                elif(types=="datatype"):
                    template+="\t\t\trr:datatype "+  objec[1] +"\n\t\t]\n\t];\n\n"
        else:
            termMap=getTermMap(object)
            if(termMap=='rr:template "'):
                object=object.replace("$",'')
                object=object.replace("(","{")
                object=object.replace(")",'}')
            else:
                object=object.replace("$(",'')
                object=object.replace(")",'')
            if(termMap!='rr:constant '):
                template+="\t\t\t"+ termMap + object + '"'+ '\n\t\t]\n\t];\n\n'
            else:
                template+="\t\t\t"+ termMap + object + '\n\t\t]\n\t];\n\n'

    elif(len(predob)==3):
        #1 pred, 2 obj, 3 datatype, leng
        template+="\t\trr:predicate "+str(predob[0])+";\n"+"\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
        object=str(predob[1])
        termMap=getTermMap(object)
        if(termMap=='rr:template "'):
            object=object.replace("$",'')
            object=object.replace("(","{")
            object=object.replace(")",'}')
        else:
            object=object.replace("$(",'')
            object=object.replace(")",'')
        if(termMap!='rr:constant '):
            template+="\t\t\t"+ termMap + object + '"'+ ';\n'
        else:
            template+="\t\t\t"+ termMap + object + ';\n'
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
        template="\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n\t\trr:predicate " + predob.get(access) +";\n"
        if "objects" in predob:
            if "value" in predob.get("objects"):
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=predob.get("objects").get("value")
                termMap=getTermMap(object)
                if(termMap=='rr:template "'):
                    object=object.replace("$",'')
                    object=object.replace("(","{")
                    object=object.replace(")",'}')
                else:
                    object=object.replace("$(",'')
                    object=object.replace(")",'')
                if(termMap!='rr:constant '):
                    template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                else:
                    template+="\t\t\t"+ termMap + object + ';\n'
                #"\t\t]\n\t];\n\n"
                if "datatype" in predob.get("objects"):
                    template+= "\t\t\trr:datatype " + predob.get("objects").get("datatype") + "\n\t\t]\n\t];\n\n"
                elif "type" in predob.get("objects"):
                    template+= "\t\t\trr:TermType " + predob.get("objects").get("type") + "\n\t\t]\n\t];\n\n"
                elif "language" in predob.get("objects"):
                    template+= '\t\t\trr:language "' + predob.get("objects").get("language") + '"\n\t\t]\n\t];\n\n'
            elif "mapping" in predob.get("objects"):
                template+= joinMapping(data,mapping,predob.get("objects"))
                print("--------------------------")
                print(template)
            else:
                if(type(predob.get("objects"))!=list):
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    object=predob.get("objects")
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n\t\t]\n\t];\n\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n\t\t]\n\t];\n\n'

                else:
                    for objec in predob.get("objects"):
                        if "mapping" in objec:
                            template+= joinMapping(data,mapping,objec)
                            continue
                        else:
                            template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                        if(type(objec) is list):
                            object = objec[0]
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        else:
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        if(termMap!='rr:constant '):
                            template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                        else:
                            template+="\t\t\t"+ termMap + object + ';\n'
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

        elif "o" in predob:
            if "value" in predob.get("o"):
                template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                object=predob.get("o").get("value")
                termMap=getTermMap(object)
                if(termMap=='rr:template "'):
                    object=object.replace("$",'')
                    object=object.replace("(","{")
                    object=object.replace(")",'}')
                else:
                    object=object.replace("$(",'')
                    object=object.replace(")",'')
                if(termMap!='rr:constant '):
                    template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                else:
                    template+="\t\t\t"+ termMap + object + ';\n'
                #"\t\t]\n\t];\n\n"
                if "datatype" in predob.get("o"):
                    template+= "\t\t\trr:datatype " + predob.get("objects").get("datatype") + "\n\t\t]\n\t];\n\n"
                elif "type" in predob.get("o"):
                    template+= "\t\t\trr:TermType " + predob.get("objects").get("type") + "\n\t\t]\n\t];\n\n"
                elif "language" in predob.get("o"):
                    template+= '\t\t\trr:language "' + predob.get("objects").get("language") + '"\n\t\t]\n\t];\n\n'
            elif "mapping" in predob.get("o"):
                template+= joinMapping(data,mapping,predob.get("o"))
            else:
                if(type(predob.get("o"))!=list):
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    object=predob.get("o")
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n\t\t]\n\t];\n\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n\t\t]\n\t];\n\n'


                else:
                    for objec in predob.get("o"):
                        if "mapping" in objec:
                            template+= joinMapping(data,mapping,objec)
                            continue
                        else:
                            template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                        if(type(objec) is list):
                            object = objec[0]
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        else:
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        if(termMap!='rr:constant '):
                            template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                        else:
                            template+="\t\t\t"+ termMap + object + ';\n'
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
        if("objects" in predob):
            if (type(predob.get("objects"))==list):
                template="\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n"
                for predic in predob.get(access):
                    template+= "\t\trr:predicate " + str(predic) + ";\n"
                if(len(predob.get("objects"))==2 and type(predob.get("objects")[1])!=list and type(predob.get("objects")[1])!=list): #solo un objeto con tipo
                    object=predob.get("objects")[0]
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')

                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n'
                    types = check_type_simple(predob.get("objects")[1])
                    if(types!="error"):
                        if(types=="iri"):
                            template+="\t\t\trr:TermType rr:IRI"+"\n\t\t];\n"
                        elif(types=="language"):
                            lenguage=predob.get("objects")[1].replace("~lang","")
                            template+='\t\t\trr:language "'+  lenguage +'"\n\t\t];\n'
                        elif(types=="datatype"):
                            template+="\t\t\trr:datatype "+  predob.get("objects")[1] +"\n\t\t];\n"
                    else:
                        raise Exception("Error: incorrect format of predicateObjectMap in mapping " + mapping)
                    template=template[:-2]
                    template+= "\n\t];\n\n"
                else:
                    for objec in predob.get("objects"):
                        template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                        if(type(objec) is list):
                            object = objec[0]
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        else:
                            object=objec
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        if(termMap!='rr:constant '):
                            template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                        else:
                            template+="\t\t\t"+ termMap + object + ';\n'
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
                if "value" in predob.get("objects"):
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    object=predob.get("objects").get("value")
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n'
                    #"\t\t]\n\t];\n\n"
                    if "datatype" in predob.get("objects"):
                        template+= "\t\t\trr:datatype " + predob.get("objects").get("datatype") + "\n\t\t]\n\t];\n\n"
                    elif "type" in predob.get("objects"):
                        template+= "\t\t\trr:TermType " + predob.get("objects").get("type") + "\n\t\t]\n\t];\n\n"
                    elif "language" in predob.get("objects"):
                        template+= '\t\t\trr:language "' + predob.get("objects").get("language") + '"\n\t\t]\n\t];\n\n'
                elif "mapping" in predob.get("objects"):
                    template+= joinMapping(data,mapping,predob.get("objects"))
                else:#creo que sobra
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    object=predob.get("objects")
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n\t\t]\n\t];\n\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n\t\t]\n\t];\n\n'



        elif ("o" in predob):
            if (type(predob.get("o"))==list):
                template="\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n"
                for predic in predob.get(access):
                    template+= "\t\trr:predicate " + str(predic) + ";\n"
                if(len(predob.get("o"))==2 and type(predob.get("o")[1])!=list and type(predob.get("o")[1])!=list): #solo un objeto con tipo
                    object=predob.get("o")[0]
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')

                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n'
                    types = check_type_simple(predob.get("o")[1])
                    if(types!="error"):
                        if(types=="iri"):
                            template+="\t\t\trr:TermType rr:IRI"+"\n\t\t];\n"
                        elif(types=="language"):
                            lenguage=predob.get("o")[1].replace("~lang","")
                            template+='\t\t\trr:language "'+  lenguage +'"\n\t\t];\n'
                        elif(types=="datatype"):
                            template+="\t\t\trr:datatype "+  predob.get("o")[1] +"\n\t\t];\n"
                    else:
                        raise Exception("Error: incorrect format of predicateObjectMap in mapping " + mapping)
                    template=template[:-2]
                    template+= "\n\t];\n\n"
                else:
                    for objec in predob.get("o"):
                        template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                        if(type(objec) is list):
                            object = objec[0]
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        else:
                            object=objec
                            termMap=getTermMap(object)
                            if(termMap=='rr:template "'):
                                object=object.replace("$",'')
                                object=object.replace("(","{")
                                object=object.replace(")",'}')
                            else:
                                object=object.replace("$(",'')
                                object=object.replace(")",'')
                        if(termMap!='rr:constant '):
                            template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                        else:
                            template+="\t\t\t"+ termMap + object + ';\n'
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
                if "value" in predob.get("o"):
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    object=predob.get("o").get("value")
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n'
                    #"\t\t]\n\t];\n\n"
                    if "datatype" in predob.get("o"):
                        template+= "\t\t\trr:datatype " + predob.get("objects").get("datatype") + "\n\t\t]\n\t];\n\n"
                    elif "type" in predob.get("o"):
                        template+= "\t\t\trr:TermType " + predob.get("objects").get("type") + "\n\t\t]\n\t];\n\n"
                    elif "language" in predob.get("o"):
                        template+= '\t\t\trr:language "' + predob.get("objects").get("language") + '"\n\t\t]\n\t];\n\n'
                elif "mapping" in predob.get("o"):
                    template+= joinMapping(data,mapping,predob.get("objects"))
                else:#creo que sobra
                    template+="\t\trr:objectMap [ \n\t\t\ta rr:ObjectMap;\n"
                    object=predob.get("o")
                    termMap=getTermMap(object)
                    if(termMap=='rr:template "'):
                        object=object.replace("$",'')
                        object=object.replace("(","{")
                        object=object.replace(")",'}')
                    else:
                        object=object.replace("$(",'')
                        object=object.replace(")",'')
                    if(termMap!='rr:constant '):
                        template+="\t\t\t"+ termMap + object + '"'+ ';\n\t\t]\n\t];\n\n'
                    else:
                        template+="\t\t\t"+ termMap + object + ';\n\t\t]\n\t];\n\n'

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

def check_type_simple(object):

    if "~iri" in object:
        return "iri"
    elif "~lang" in object:
        return "language"
    elif ("xsd:" in object) or ("ex:" in object):
        return "datatype"
    else:
        return "error"


def joinMapping(data,mapping,objec):
    list_mappings=[]
    template=""
    for mappings in data.get("mappings"):
        list_mappings.append(mappings)

    if objec.get("mapping") in list_mappings:
        subject_list = subjectmod.addSubject(data, objec.get("mapping"))
        list_initial_sources= sourcemod.getInitialSources(data)
        source_list=sourcemod.addSource(data,objec.get("mapping"),list_initial_sources)

        sumSourSub = len(subject_list) * len(source_list)
        for i in range(sumSourSub):
            template+="\t\trr:objectMap [ \n\t\t\ta rr:RefObjectMap;\n\t\t\trr:parentTriplesMap <#"+ objec.get("mapping")+"_"+str(i)+">;\n"
            if "condition" in objec:
                if "parameters" in objec.get("condition"):
                    list_parameters = objec.get("condition").get("parameters")
                    if len(list_parameters)==2:
                        child=list_parameters[0][1]
                        parent=list_parameters[1][1]
                        child=child.replace("$(",'"')
                        child=child.replace(")",'"')
                        parent=parent.replace("$(",'"')
                        parent=parent.replace(")",'"')

                        template+='\t\t\trr:joinCondition [\n\t\t\t\trr:child ' + child + ';\n\t\t\t\trr:parent ' + parent + ';\n\t\t\t]\n\t\t];\n'

                    else:
                            raise Exception("Error: more than two parameters in join condition in mapping1 " + mapping)
            else:
                template+="\n\t\t]\n\t];"
                return template


    else:
        raise Exception("Error in reference mapping another mapping in mapping " + mapping)

    return template



def getTermMap(text):
    if("$(" in text and ")" in text):
        if text[0]=="$":
            return 'rml:reference "'
        else:
            return 'rr:template "'
    else:
        return 'rr:constant '
