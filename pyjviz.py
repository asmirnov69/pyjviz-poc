import ipdb
import typer, sys

import collections
import html
import sys

import rdflib
import rdflib.extras.cmdlineutils
from rdflib import XSD

app = typer.Typer()

@app.command()
def dump_dot(pyjlog_ttl_fn):
    g = rdflib.Graph()
    g.parse(pyjlog_ttl_fn)

    out_fd = sys.stdout
    print('digraph { node [ fontnme = "DejaVu Sans" ] ;', file = out_fd)

    nodes = {}; node_c = 0
    for s, _ in g.query("select ?s ?s { ?s rdf:type <pyj:DataFrame> }"):
        if not s in nodes:
            nodes[s] = node_c
            print(f'node{node_c} [ label = "{s.toPython()}" ]', file = out_fd)
            node_c += 1

    for s, mn in g.query("select ?s ?mn { ?s rdf:type <pyj:Method>; rdf:label ?mn }"):
        if not s in nodes:
            nodes[s] = node_c
            print(f'node{node_c} [ label = "{mn.toPython()}" ]', file = out_fd)
            node_c += 1

    #ipdb.set_trace()
    for df, method_call in g.query("select ?df ?m { ?df <pyj:method-call>|<pyj:method-call-arg> ?m }"):
        df = nodes[df]; m = nodes[method_call]
        print(f"node{df} -> node{m}", file = out_fd)

    for method_ret, df in g.query("select ?m ?df { ?m <pyj:method-return> ?df }"):
        df = nodes[df]; m = nodes[method_ret]
        print(f"node{m} -> node{df}", file = out_fd)
        
    print("}", file = out_fd)


if __name__ == "__main__":
    app()
