# pyjviz module implements basic visualisation of pyjviz rdf log
# there is no dependency of this code to other part of pyjanitor
#
import os.path
import collections
import html
import sys

import rdflib
from io import StringIO

import graphviz as gv

def dump_dot_code(g):
    #ipdb.set_trace()
    cmcs = [r for r in g.query("select ?pp ?pl { ?pp rdf:type <pyj:CMC>; rdf:label ?pl }")]

    out_fd = StringIO()
    
    print("""
    digraph G {
    rankdir = "LR"
    fontname="Helvetica,Arial,sans-serif"
    node [ 
      style=filled
      shape=rect
      pencolor="#00000044" // frames color
      fontname="Helvetica,Arial,sans-serif"
      shape=plaintext
    ]
    edge [fontname="Helvetica,Arial,sans-serif"]    
    """, file = out_fd)
    #print('rankdir = "TB"', file = out_fd)

    cmc_c = 0
    for cmc, cmc_label in cmcs:
        nodes = {}; node_c = 0
        for s, s_shape, s_col in g.query("select ?s ?s_shape ?s_col { ?s rdf:type <pyj:DataFrame>; <pyj:df-shape> ?s_shape; <pyj:df-columns> ?s_col; <pyj:cmc> ?cmc}", initBindings = {'cmc': cmc}):
            if not s in nodes:
                nodes[s] = f'{cmc_c}_{node_c}'
                cols = "\n".join(['<tr><td align="left"><FONT POINT-SIZE="8px">' + html.escape(x) + "</FONT></td></tr>" for x in s_col.toPython().split(",")])
                print(f"""node{cmc_c}_{node_c} [ 
                color="#88000022"
                shape = rect
                label = <<table border="0" cellborder="0" cellspacing="0" cellpadding="4">
                         <tr> <td> <b>{s.toPython()}</b><br/>shape: {s_shape.toPython()}</td> </tr>
                         <tr> <td align="left"><i>columns:</i><br align="left"/></td></tr>
                {cols}
                         </table>>
                ];""", file = out_fd)
                node_c += 1

        for s, mn in g.query("select ?s ?mn { ?s rdf:type <pyj:Method>; rdf:label ?mn; <pyj:cmc> ?cmc }", initBindings = {'cmc': cmc}):
            if not s in nodes:
                nodes[s] = f'{cmc_c}_{node_c}'
                print(f'node{cmc_c}_{node_c} [ label = "{mn.toPython()}" ];', file = out_fd)
                node_c += 1

        #ipdb.set_trace()
        if cmc_label.toPython() != "none":
            print(f'subgraph cluster_{cmc_c} {{', file = out_fd); cmc_c += 1
            print(f'label = "{cmc_label.toPython()}";', file = out_fd)
        
        for df, method_call in g.query("select ?df ?m { ?df <pyj:method-call>|<pyj:method-call-arg> ?m. ?df <pyj:cmc> ?cmc. ?m <pyj:cmc> ?cmc }", initBindings = {'cmc': cmc}):
            df = nodes[df]; m = nodes[method_call]
            print(f"node{df} -> node{m};", file = out_fd)

        for method_ret, df in g.query("select ?m ?df { ?m <pyj:method-return> ?df. ?df <pyj:cmc> ?cmc. ?m <pyj:cmc> ?cmc }", initBindings = {'cmc': cmc}):
            df = nodes[df]; m = nodes[method_ret]
            print(f"node{m} -> node{df};", file = out_fd)
            
        if cmc_label.toPython() != "none":
            print("}", file = out_fd)
            
    print("}", file = out_fd)

    return out_fd.getvalue()

def get_rdflog_filename(argv0):
    rdflog_fn = os.path.basename(argv0).replace(".py", ".ttl")
    return os.path.join("rdflog", rdflog_fn)

def render_rdflog(rdflog_ttl_fn, verbose = True):
    g = rdflib.Graph()
    g.parse(rdflog_ttl_fn)

    dot_code = dump_dot_code(g)
    gv_src = gv.Source(dot_code)
    gv_src.render(rdflog_ttl_fn + '.dot', format = 'png', engine = 'dot')

    if verbose:
        print(f"\nsaved diagram file {rdflog_ttl_fn + '.dot' + '.png'}")
    
