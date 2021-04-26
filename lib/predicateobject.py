
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
