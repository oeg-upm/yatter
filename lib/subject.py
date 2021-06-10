import yaml

def addSubject(data, mapping):
    list_subject=[]
    final_list=[]

    if ("s" in data.get("mappings").get(mapping)):
        list_subject=data.get("mappings").get(mapping).get("s")
        if (type(list_subject)== list): #varios sujetos
            for subject in list_subject:
                subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
                termMap=getTermMap(subject)
                if(termMap=='rr:template "'):
                    subject=subject.replace("$",'')
                    subject=subject.replace("(","{")
                    subject=subject.replace(")",'}')
                else:
                    subject=subject.replace("$(",'')
                    subject=subject.replace(")",'')
                if(termMap!='rr:constant '):
                    subject_template+= termMap + ' "'+ subject + '"'+ "\n\t];\n\n"
                else:
                    subject_template+= termMap + subject + "\n\t];\n\n"
                final_list.append(subject_template)


        else: #un solo sujeto
            subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
            subject=list_subject
            termMap=getTermMap(subject)
            if(termMap=='rr:template "'):
                subject=subject.replace("$",'')
                subject=subject.replace("(","{")
                subject=subject.replace(")",'}')
            else:
                subject=subject.replace("$(",'')
                subject=subject.replace(")",'')
            if(termMap!='rr:constant '):
                subject_template+= termMap + ' "'+ subject + '"'+ "\n\t];\n\n"
            else:
                subject_template+= termMap + subject + "\n\t];\n\n"
            final_list.append(subject_template)


    elif ("subjects" in data.get("mappings").get(mapping)):
        list_subject= data.get("mappings").get(mapping).get("subjects")
        if (type(list_subject)== list): #varios sujetos
            for subject in list_subject:
                subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
                termMap=getTermMap(subject)
                if(termMap=='rr:template "'):
                    subject=subject.replace("$",'')
                    subject=subject.replace("(","{")
                    subject=subject.replace(")",'}')
                else:
                    subject=subject.replace("$(",'')
                    subject=subject.replace(")",'')
                if(termMap!='rr:constant '):
                    subject_template+= termMap + ' "'+ subject + '"'+ "\n\t];\n\n"
                else:
                    subject_template+= termMap + subject + "\n\t];\n\n"
                final_list.append(subject_template)


        else: #un solo sujeto
            subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
            subject=list_subject
            termMap=getTermMap(subject)
            if(termMap=='rr:template "'):
                subject=subject.replace("$",'')
                subject=subject.replace("(","{")
                subject=subject.replace(")",'}')
            else:
                subject=subject.replace("$(",'')
                subject=subject.replace(")",'')
            if(termMap!='rr:constant '):
                subject_template+= termMap + ' "'+ subject + '"'+ "\n\t];\n\n"
            else:
                subject_template+= termMap + subject + "\n\t];\n\n"
            final_list.append(subject_template)


    elif ("subject" in data.get("mappings").get(mapping)):
        list_subject=data.get("mappings").get(mapping).get("subject")
        if (type(list_subject)== list): #varios sujetos ERROR
            raise Exception("ERROR: Only one subject should be in mapping: " + mapping)

        else: #un solo sujeto
            subject_template = "\trr:subjectMap [\n" + "\t\ta rr:SubjectMap;\n"+ "\t\t"
            subject=list_subject
            termMap=getTermMap(subject)
            if(termMap=='rr:template "'):
                subject=subject.replace("$",'')
                subject=subject.replace("(","{")
                subject=subject.replace(")",'}')
            else:
                subject=subject.replace("$(",'')
                subject=subject.replace(")",'')
            if(termMap!='rr:constant '):
                subject_template+= termMap + ' "'+ subject + '"'+ "\n\t];\n\n"
            else:
                subject_template+= termMap + subject + "\n\t];\n\n"
            final_list.append(subject_template)


    else:
        raise Exception("ERROR: no subjects in mapping " + mapping)


    return final_list



def getTermMap(text):
    if("$(" in text and ")" in text):
        if text[0]=="$":
            return "rml:reference "
        else:
            return "rr:template "
    else:
        return "rr:constant "
