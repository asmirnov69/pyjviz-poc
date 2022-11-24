import sys
import rdflib

if __name__ == "__main__":
    rdflog_ttl_fn = sys.argv[1]
    g = rdflib.Graph()
    g.parse(rdflog_ttl_fn)
    print(g)
    for spo in g:
        print(spo)
        
