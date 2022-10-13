import ipdb
import typer, sys, os

import collections
import html
import sys

import rdflib
import graphviz as gv
from io import StringIO

import janitor.pyjviz as pyjviz

app = typer.Typer()
        
@app.command()
def dump_dot(pyjlog_ttl_fn):
    g = rdflib.Graph()
    g.parse(pyjlog_ttl_fn)

    dot_code = pyjviz.dump_dot_code(g)
    gv_src = gv.Source(dot_code)
    gv_src.render('./test-pyjviz', format = 'png', engine = 'dot')
    os.unlink('./test-pyjviz')
    
if __name__ == "__main__":
    app()
