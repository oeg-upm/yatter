import yaml


def getInitialSources(data):
    list_initial_sources =[]
    if "sources" in data:
        for y in data.get("sources"):
            list_initial_sources.append(y)
    return list_initial_sources


def addSource(data, mapping,list_initial_sources):

    source_template=""
    list_sources=[]
    final_list=[]
    #primero se comprueba que este en la lista inicial de sources, sino luego se comprueba si es forma completa o simplificada
    if "sources" in data.get("mappings").get(mapping):
        if(type(data.get("mappings").get(mapping).get("sources")) is str ):
            #list_sources.append(data.get("mappings").get(mapping).get("sources"))
            final_list.append(addInitialSource(data,data.get("mappings").get(mapping).get("sources")))
        else:
            for sources in data.get("mappings").get(mapping).get("sources"):
                list_sources.append(sources)
            for sources in list_sources:
                if sources in list_initial_sources:
                    final_list.append(addInitialSource(data,sources))
    elif "source" in data.get("mappings").get(mapping):
        if(type(data.get("mappings").get(mapping).get("source")) is str ):
            #list_sources.append(data.get("mappings").get(mapping).get("source"))
            final_list.append(addInitialSource(data,data.get("mappings").get(mapping).get("source")))
        else:
            for sources in data.get("mappings").get(mapping).get("source"):
                list_sources.append(sources)
            for sources in list_sources:
                if sources in list_initial_sources:
                    final_list.append(addInitialSource(data,sources))
    else:
        raise Exception("ERROR: sources not defined in mapping " + mapping)

    if "sources" in data.get("mappings").get(mapping):
        if (type(data.get("mappings").get(mapping).get("sources")) is not str):
            for sources in data.get("mappings").get(mapping).get("sources"):
                if "access" in sources:
                    final_list.append(addSourceFull(data,mapping,sources))
                elif type(sources) is list:
                    final_list.append(addSourceSimplified(data,mapping,sources))
                elif sources not in list_initial_sources:
                    raise Exception("ERROR: source " + sources + " in mapping "+ mapping + " not valid")
    else:
        if (type(data.get("mappings").get(mapping).get("source")) is not str):
            for sources in data.get("mappings").get(mapping).get("source"):
                if "access" in sources:
                    final_list.append(addSourceFull(data,mapping,sources))
                elif type(sources) is list:
                    final_list.append(addSourceSimplified(data,mapping,sources))
                elif sources not in list_initial_sources:
                    raise Exception("ERROR: source " + sources + " in mapping "+ mapping + " not valid")
    return final_list

def addInitialSource(data,sources):
    source_template = ""
    if "query" in sources:
        list_source=databaseSource(data,mapping,sources)
        return list_source

    if "access" in data.get("sources").get(sources):
        access = data.get("sources").get(sources).get("access")
        str_access = str(access)
        extension = str_access.split('.')
    elif type(data.get("sources").get(sources)) is list:
        source_list = data.get("sources").get(sources)
        source_template = "\trml:logicalSource [\n" +"\t\ta rml:logicalSource;\n" + "\t\trml:source "
        source= source_list[0][0]
        source_aux = source.split('~')
        source_aux1= source_aux[0].split('.')
        source_name = source_aux1[0]
        source_extension = source_aux1[1]
        source_referenceFormulation = source_aux[1]
        if(checkExtension(source_extension,source_referenceFormulation)==1):
            raise Exception("ERROR: mismatch extension and referenceFormulation in source "+ sources )
        else:
            if len(source_list[0])== 1:
                if (source_extension=="csv" or source_extension=="SQL2008"): #THE EXTENSION OF DATABASES COULD DE WRONG  instead of extension could be referenceFormulation?
                    source_template+= '"'+source_name + '"'+";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + "\n" +  "\t];\n"
                else:
                    raise Exception("ERROR: source " + sources + " has no iterator")
            else:
                source_delim = source_list[0][1]
                source_template+= '"'+source_name+'"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + ";\n" + '\t\trml:iterator "' +source_delim + '"'+ ";\n\t];\n"
        return source_template
    else:
        raise Exception("ERROR: source "+ sources + " is incorrect")

    source_template = "\trml:logicalSource [\n" +"\t\ta rml:logicalSource;\n" + "\t\trml:source "
    if "referenceFormulation" in data.get("sources").get(sources):
        source_referenceFormulation = data.get("sources").get(sources).get("referenceFormulation")
        if checkExtension(extension[1],source_referenceFormulation)==1:
            raise Exception("ERROR: mismatch extension and referenceFormulation in source "+ sources )
        if getReferenceFOrmulation(source_referenceFormulation)!= "ERROR":
            source_referenceFormulation=getReferenceFOrmulation(source_referenceFormulation)
        #hfew=( sources + source_referenceFormulation) #It's no use, but if it's not there it will not work

    else:
        #ver si es csv
        if (extension[1]=="csv"):
            if "iterator" in data.get("sources").get(sources):
                source_iterator = data.get("sources").get(sources).get("iterator")
                source_template += '"' + access + '";\n' + '\t\trml:iterator "' +source_iterator + '\n\t];\n'
                return source_template
            else:
                source_template += '"' + access + '";\n' + '\t];\n'
                return source_template
        else:
            raise Exception("ERROR: source " + sources + "has no referenceFormulation")
    if "iterator" in data.get("sources").get(sources):
        source_iterator = data.get("sources").get(sources).get("iterator")
        source_template += '"' + access + '";\n' + "\t\trml:referenceFormulation ql:"+ source_referenceFormulation +";\n" + '\t\trml:iterator "' +source_iterator + '"\n\t];\n'
        return source_template
    else:
        if(extension[1]=="csv" or extension[1]=="SQL2008"):
            source_template += '"' + access + '";\n' + "\t\trml:referenceFormulation ql:"+ source_referenceFormulation +";\n" + '\t];\n'
            return source_template
        else:
            raise Exception("ERROR: source " + sources + " has no iterator")

def addSourceSimplified(data,mapping,sources):
    source_template = "\trml:logicalSource [\n" +"\t\ta rml:logicalSource;\n" + "\t\trml:source "
    source= sources[0]
    source_aux = source.split('~')
    source_aux1= source_aux[0].split('.')
    source_name = source_aux1[0]
    source_extension = source_aux1[1]
    source_referenceFormulation = source_aux[1]
    if(checkExtension(source_extension,source_referenceFormulation)==1):
        raise Exception("ERROR: mismatch extension and referenceFormulation in source "+ sources + " in mapping "+mapping)
    else:
        if len(sources)== 1:
            if (source_extension=="csv" or source_extension=="SQL2008"): #THE EXTENSION OF DATABASES COULD DE WRONG  instead of extension could be referenceFormulation?
                source_template+= '"'+source_aux[0]+'"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + "\n" +  "\t];\n"
            else:
                raise Exception("ERROR: source " + sources + " in mapping " + mapping +" has no iterator")
        else:
            source_delim = sources[1]
            source_template+= '"'+source_aux[0]+'"' + ";\n" + "\t\trml:referenceFormulation ql:" + source_referenceFormulation + ";\n" + '\t\trml:iterator "' +source_delim + '"'+ ";\n\t];\n"
    return source_template

def addSourceFull(data,mapping,sour):
    source_final=""
    if "query" in sour:
        list_source=databaseSource(data,mapping,sour)
        return list_source
    list_sources=[]
    list_sources.append("sources")
    list_sources.append(data.get("mappings").get(mapping).get("sources"))
    source_template = "\trml:logicalSource [\n" +"\t\ta rml:logicalSource;\n" + "\t\trml:source "
    if "access" in sour:
        source = str(sour.get("access"))
        extension = source.split(".")
    else:
        raise Exception('ERROR: source' +sour.get("access") + 'in mapping ' + mapping+' has no "access"')

    if "referenceFormulation" in sour:
        source_referenceFormulation = str(sour.get("referenceFormulation"))
        if checkExtension(extension[1],source_referenceFormulation)==1:
            raise Exception("ERROR: mismatch extension and referenceFormulation in source " + sour.get("access") + "in mapping " + mapping)
        if getReferenceFOrmulation(source_referenceFormulation)!= "ERROR":
            source_referenceFormulation=getReferenceFOrmulation(source_referenceFormulation)
    else:
        if(extension[1]=="csv"):
            if "iterator" in sour:
                source_iterator = str(sour.get("iterator"))
                source_template += '"'+source+'"' + ";\n" + '\t\trml:iterator "' +source_iterator + '"\n\t];\n'
                return source_template
            else:
                source_template += '"'+source+'"' + ";\n" + '"\n\t];\n'
                return source_template
        else:
            raise Exception("ERROR: source "+sour.get("access") + "in mapping " + mapping + " has no referenceFormulation")
    if "iterator" in sour:
        source_iterator = str(sour.get("iterator"))
        source_template += '"'+source+'"' + ";\n" + "\t\trml:referenceFormulation ql:"+ source_referenceFormulation +";\n" + '\t\trml:iterator "' +source_iterator + '"\n\t];\n'
    else:
        if (extension[1]=="csv" or extension[1]=="SQL2008"):
            source_template += '"'+source+'"' + ";\n" + "\t\trml:referenceFormulation ql:"+ source_referenceFormulation +";\n" + '"\n\t];\n'
        else:
            raise Exception("ERROR: source "+sour.get("access") + " in mapping " + mapping + " has no iterator")
    source_final += source_template
    return source_final

def checkExtension (extension,referenceFormulation):
    switcher={
        "json":"jsonpath",
        "csv":"csv",
        "xml":"xpath"
        #para querys
    }
    reference = switcher.get(extension,"ERROR")
    if reference == referenceFormulation:
        return 0
    else:
        return 1

def getReferenceFOrmulation (referenceFormulation):
    switcher={
        "jsonpath":"JSONPath",
        "csv":"CSV",
        "xpath":"XPath"
    }
    return switcher.get(referenceFormulation,"ERROR")


def databaseSource(data,mapping,source):
    list=[]
    templatelog="\trml:logicalSource [\n\t\ta rml:LogicalSource;\n"
    if "access" in source:
        if "credentials" in source:
            if "type" in source and source.get("type")=="mysql":
                templatelog+='\t\trml:source <#DataSource_'+mapping+'>;\n\t\trr:sqlVersion rr:SQL2008;\n\t\trml:query "'+source.get("query") +'";\n\t\t'
                if "referenceFormulation" in source:
                    formu=getReferenceFOrmulation(source.get("referenceFormulation"))
                    templatelog+="\t\trml:referenceFormulation ql:"+ formu +"\n\t];\n"
                else:
                    templatelog+="\n\t];\n"

        else:
            raise Exception("ERROR: no credentials to get access to source in mapping "+ mapping)
    else:
        raise Exception("ERROR: no access to the source in mapping " + mapping)


    list.append(templatelog)

    templateDat = '<#DataSource_'+mapping+'> a d2rq:Database;\n\tdrr1:jdbcDSN "'+ source.get("access")+'";\n\td2rq:jdbcDriver "com.mysql.jdbc.Driver";\n\td2rq:username "'+source.get("credentials").get("username")+'";\n\td2rq:password "'+source.get("credentials").get("password")+'".\n\n'

    list.append(templateDat)

    return list
