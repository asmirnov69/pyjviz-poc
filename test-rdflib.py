import ipdb
import rdflib

if __name__ == "__main__":
    g = rdflib.Graph()
    g.parse("./test-rdf.ttl")
    print(len(g))

    q_res = g.query("select * {?s ?p ?o}")
    print("\n".join([f"{r}" for r in q_res]))
    
