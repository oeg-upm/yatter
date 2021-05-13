import yaml

def addMapping(data, mapping,it):
    map_template="<#"+mapping+"_"+str(it)+"> a rr:TriplesMap;\n\n"
    return map_template

def addPrefix(data):
    template=""
    if "prefixes" in data:
        prefixes=data.get("prefixes")
        for prefix in prefixes:
            template+="@prefix "+ prefix +": <"+data.get("prefixes").get(prefix)+">.\n"
        template+="\n\n"
        return template
    else:
        return template
