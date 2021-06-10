import lib.main as functions
from os import listdir, walk
from os.path import isfile, join
from rdflib import Graph, ConjunctiveGraph, compare

if __name__ == "__main__":

    f = []
    list = []
    for (dirpath, dirnames, filenames) in walk("./test"):
        if filenames and "mapping.yml" in filenames:
            print("testing " + dirpath)
            yarrrml = functions.open_inputs(dirpath + "/mapping.yml")
            rml_output = functions.translate(yarrrml)
            rml_output_path = open(dirpath + "/mapping-output.rml.ttl", "w")
            rml_output_path.write(rml_output)
            expected_output_graph = ConjunctiveGraph()
            output_graph = ConjunctiveGraph()
            try:
                expected_output_graph.parse(dirpath + "/mapping.rml.ttl", format="turtle")
                output_graph.parse(dirpath + "/mapping-output.rml.ttl", format="turtle")
                iso_expected = compare.to_isomorphic(expected_output_graph)
                iso_output = compare.to_isomorphic(output_graph)
                # and graphs are equal
                if iso_expected == iso_output:
                    result = "passed"
                # and graphs are distinct
                else:
                    print("Output RDF does not match with the expected RDF")
                    result = "failed"
                list.append(dirpath + "," + results)
            except Exception as e:
                print(str(e))
                results = "failed"
                list.append(dirpath + "," + results + ", " + str(e))

    for result in list:
        print(result)
