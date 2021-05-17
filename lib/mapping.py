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
        if "rr" not in data.get("prefixes"):
            template+="@prefix rr: <http://www.w3.org/ns/r2rml#>."
        if "rml" not in data.get("prefixes"):
            template+="@prefix rml: <http://semweb.mmlab.be/ns/rml#>."
        if "rdf" not in data.get("prefixes"):
            template+="@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>."
        template+="\n\n"
        return template
    else:
        return template
