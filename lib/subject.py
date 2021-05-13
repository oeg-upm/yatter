import yaml

def addSubject(data, mapping):
    subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
    list_subject=[]
    list_subject.append("s")
    final_list =[]
    if ("s" in data.get("mappings").get(mapping) ):
        list_subject.append(data.get("mappings").get(mapping).get("s"))
        if(len(list_subject[1][0])==1):
            #un solo sujeto
            subject = "".join(data.get("mappings").get(mapping).get("s"))
            termMap=getTermMap(subject)
            subject=subject.replace("$(","{").replace(")","}")
            subject_template = subject_template + termMap+' "'  + subject +'"'+ "\n\t];"+"\n\n"
            final_list.append(subject_template)
            return final_list
        else:
            #varios sujetos
            for x in list_subject[1]:
                subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
                termMap=getTermMap(x)
                x = x.replace("$(","{").replace(")","}")
                subject_template = subject_template + termMap+' "'  + x +'"'+ "\n\t];"+"\n\n"
                final_list.append(subject_template)
            return final_list

    else:
        if("subjects" in data.get("mappings").get(mapping)):
            list_subject.append(data.get("mappings").get(mapping).get("subjects"))
            if(len(list_subject[1][0])==1):
                #un solo sujeto
                subject = "".join(data.get("mappings").get(mapping).get("subjects"))
                termMap=getTermMap(subject)
                subject=subject.replace("$(","{").replace(")","}")
                subject_template = subject_template+ termMap + ' "'  + subject +'"'+ "\n\t];"+"\n\n"
                final_list.append(subject_template)
                return final_list
            else:
                #varios sujetos
                for x in list_subject[1]:
                    termMap=getTermMap(subject)
                    subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
                    x = x.replace("$(","{").replace(")","}")
                    subject_template = subject_template +termMap+ ' "'  + x +'"'+ "\n\t];"+"\n\n"
                    final_list.append(subject_template)
                return final_list

        elif ("subject" in data.get("mappings").get(mapping)):
            list_subject.append(data.get("mappings").get(mapping).get("subject"))
            if(len(list_subject[1][0])==1):
                #un solo sujeto
                subject = "".join(data.get("mappings").get(mapping).get("subject"))
                termMap=getTermMap(subject)
                subject=subject.replace("$(","{").replace(")","}")
                subject_template = subject_template+termMap + ' "'  + subject +'"'+ "\n\t];"+"\n\n"
                final_list.append(subject_template)
                return final_list
            else:
                #varios sujetos
                for x in list_subject[1]:
                    termMap=getTermMap(subject)
                    subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
                    x = x.replace("$(","{").replace(")","}")
                    subject_template = subject_template+termMap + ' "'  + x +'"'+ "\n\t];"+"\n\n"
                    final_list.append(subject_template)
                return final_list
        else:
            raise Exception("ERROR: no subjects in mapping " + mapping)

def getTermMap(text):
    if("$(" in text and ")" in text):
        if text[0]=="$":
            return "rml:reference "
        else:
            return "rr:template "
    else:
        return "rr:constant "
