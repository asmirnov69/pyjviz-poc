#import ipdb
import typer, sys
sys.path.append("..")

import collections
import html
import sys

import rdflib
import graphviz as gv
from io import StringIO

import janitor.pyjviz as pyjviz

#app = typer.Typer()
        
#@app.command()
def dump_dot():
    rdflog_ttl_fn = "./rdflog.ttl"
    #ipdb.set_trace()
    g = rdflib.Graph()
    g.parse(rdflog_ttl_fn)

    dot_code = pyjviz.dump_dot_code(g)
    gv_src = gv.Source(dot_code)
    gv_src.render(rdflog_ttl_fn + '.dot', format = 'png', engine = 'dot')
    
if __name__ == "__main__":
    #app()
    dump_dot()
    
