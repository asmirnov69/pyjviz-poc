import collections
import html
import sys

import rdflib
from io import StringIO

def dump_dot_code(g):
    #ipdb.set_trace()
    pipes = [r for r in g.query("select ?pp ?pl { ?pp rdf:type <pyj:Pipe>; rdf:label ?pl }")]

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

    pipe_c = 0
    for pipe, pipe_label in pipes:        
        nodes = {}; node_c = 0
        for s, s_shape, s_col in g.query("select ?s ?s_shape ?s_col { ?s rdf:type <pyj:DataFrame>; <pyj:df-shape> ?s_shape; <pyj:df-columns> ?s_col; <pyj:pipe> ?pp}", initBindings = {'pp': pipe}):
            if not s in nodes:
                nodes[s] = f'{pipe_c}_{node_c}'
                cols = "\n".join(['<tr><td align="left"><FONT POINT-SIZE="8px">' + html.escape(x) + "</FONT></td></tr>" for x in s_col.toPython().split(",")])
                print(f"""node{pipe_c}_{node_c} [ 
                color="#88000022"
                shape = rect
                label = <<table border="0" cellborder="0" cellspacing="0" cellpadding="4">
                         <tr> <td> <b>{s.toPython()}</b><br/>shape: {s_shape.toPython()}</td> </tr>
                         <tr> <td align="left"><i>columns:</i><br align="left"/></td></tr>
                {cols}
                         </table>>
                ];""", file = out_fd)
                node_c += 1

        for s, mn in g.query("select ?s ?mn { ?s rdf:type <pyj:Method>; rdf:label ?mn; <pyj:pipe> ?pp }", initBindings = {'pp': pipe}):
            if not s in nodes:
                nodes[s] = f'{pipe_c}_{node_c}'
                print(f'node{pipe_c}_{node_c} [ label = "{mn.toPython()}" ];', file = out_fd)
                node_c += 1

        #ipdb.set_trace()
        if pipe_label.toPython() != "none":
            print(f'subgraph cluster_{pipe_c} {{', file = out_fd); pipe_c += 1
            print(f'label = "{pipe_label.toPython()}";', file = out_fd)
        
        for df, method_call in g.query("select ?df ?m { ?df <pyj:method-call>|<pyj:method-call-arg> ?m. ?df <pyj:pipe> ?pp. ?m <pyj:pipe> ?pp }", initBindings = {'pp': pipe}):
            df = nodes[df]; m = nodes[method_call]
            print(f"node{df} -> node{m};", file = out_fd)

        for method_ret, df in g.query("select ?m ?df { ?m <pyj:method-return> ?df. ?df <pyj:pipe> ?pp. ?m <pyj:pipe> ?pp }", initBindings = {'pp': pipe}):
            df = nodes[df]; m = nodes[method_ret]
            print(f"node{m} -> node{df};", file = out_fd)
            
        if pipe_label.toPython() != "none":
            print("}", file = out_fd)
            
    print("}", file = out_fd)

    return out_fd.getvalue()
