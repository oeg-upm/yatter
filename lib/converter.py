import yaml

import mapping as mappingmod
import source as sourcemod
import subject as subjectmod

#################################LISTA DE COSAS A COMPROBAR#############################################
#se pueden poner varias sources en el mismo mapping o hay que generar un nuevo mapping second source?
#EN caso de que se puedan poner varios: habría que separarlos entre []; o [].?
#EL orden en el que aparecen las sources importa?

'''
def addPredicateObject(data,mapping):
    po_template = "\trr:predicateObjectMap [\n" + "\t\ta rr:PredicateObjectMap;\n"+ "\t\trr:template"
    if ("predicateobjects" in data.get("mappings").get(mapping)):
        if "predicate" in data.get("mappings").get(mapping).get("predicateobjects"):
            #full
            print("hola1")
        elif "p" in data.get("mappings").get(mapping).get("predicateobjects"):
            #full con acceso a p
            print("hola2")
        else:
            for po in data.get("mappings").get(mapping).get("predicateobjects"):
                if type(po) is list:
                    #simplificada
                    print(po)
                else:
                    #ERROR
                    print("hola3")

    elif ("po" in data.get("mappings").get(mapping)):
        if "predicate" in data.get("mappings").get(mapping).get("po"):
            #full
            print("hola4")
        elif "p" in data.get("mappings").get(mapping).get("po"):
            #full con acceso a p
            print("hola5")
        else:
            for po in data.get("mappings").get(mapping).get("po"):
                if type(po) is list:
                    #simplificada
                    print(po)
                else:
                    #ERROR
                    print("hola6")
    else:
        #¿ERROR?
        print("hola7")


    return po_template

def addPredicateObjectSimplified(data,mapping,po)
    po_template =""

    if(len(po)==2):
        if po[0] is list:
            #varios en uno
        else:
            ##solo predicado y objeto
    elif(len(po)==3):
        #1 pred, 2 obj, 3 datatype, leng
    else:
        #ERROR

def addPredicateObjectFull(data,mapping)

'''


print("Introduce the .yml file you want to convert to RML")
file = input()
print("\n")
#../test/example1/rml/mapping.yml
with open(file) as f:
    print("Name for your file:")
    end=input()
    nuevo_fich=open(end+".rml","a")
    print("\n")
    data = yaml.safe_load(f)
    yaml_stream = True
    print("------------------------START RML-------------------------------")
    mapping_list=[]
    list_initial_sources= sourcemod.getInitialSources(data)
    for mapp in data.get("mappings"):
        try:
            subject = subjectmod.addSubject(data, mapp)
            source_list=[]
            source_list=sourcemod.addSource(data,mapp,list_initial_sources)
            #pred =addPredicateObject(data,x)
            it = 0
            for source in source_list:
                map=mappingmod.addMapping(data,mapp,it)
                final = map + source +subject
                final = final[:-3]
                final+= ".\n"
                print(final)
                nuevo_fich.write(final)
                it=it+1
        except Exception as e:
            print(str(e))
            break
    print("FILE SUCCESFULY CREATED!")

    print("------------------------END RML-------------------------------")
