import rdflib

g = rdflib.Graph()
#result = g.parse('trees.ttl')
#result = g.parse('trees.ttl', format='ttl')
result = g.parse('prueba.rml.ttl', format='n3')
print (len(g))
for stmt in g:
    print (stmt)
