#import ipdb
import rdflib
if 0:
    import rdflib.extras.external_graph_libs as rdfxtr
    import networkx as nx
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('TkAgg') # sudo apt install python3-tk

if __name__ == "__main__":
    g = rdflib.Graph()
    g.parse("./test-rdf.ttl")
    print(len(g))

    q_res = g.query("select ?s ?p ?o {filter(?p != <pyj:pipe_head>) ?s ?p ?o }")
    #q_res = g.query("select ?s ?p ?o {?s ?p ?o }")
    print("\n".join([f"{r}" for r in q_res]))

    if 0:
        G = rdfxtr.rdflib_to_networkx_multidigraph(g)
        
        pos = nx.spring_layout(G, scale = 2)
        edge_labels = nx.get_edge_attributes(G, 'r')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
        nx.draw(G, with_labels = True)
        
        plt.show()
    
