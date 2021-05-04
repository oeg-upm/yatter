import yaml

import mapping as mappingmod
import source as sourcemod
import subject as subjectmod
import predicateobject as predicateobjectmod

#################################LISTA DE COSAS A COMPROBAR#############################################
#que hacer si tenemos $($.) en un predicateobject
#-------
print("Introduce the .yml file you want to convert to RML")
file = input()
#file="../test/EjemploYARRML.YML"
print("\n")
#../test/example1/rml/mapping.yml
with open(file) as f:
    print("Name for your file:")
    end=input()
    #end="prueba"
    nuevo_fich=open(end+".rml","a")
    data = yaml.safe_load(f)
    yaml_stream = True
    print("------------------------START RML-------------------------------")
    mapping_list=[]
    list_initial_sources= sourcemod.getInitialSources(data)
    for mapp in data.get("mappings"):
        try:
            subject_list=[]
            subject_list = subjectmod.addSubject(data, mapp)
            source_list=[]
            source_list=sourcemod.addSource(data,mapp,list_initial_sources)
            pred =predicateobjectmod.addPredicateObject(data,mapp)
            it = 0
            for source in source_list:
                for subject in subject_list:
                    map=mappingmod.addMapping(data,mapp,it)
                    final = map + source +subject + pred
                    final = final[:-3]
                    final+= ".\n"
                    print(final)
                    nuevo_fich.write(final)
                    it=it+1
        except Exception as e:
            print(str(e))
            break

    print("------------------------END RML-------------------------------")
    print("FILE SUCCESSFULY CREATED!")
