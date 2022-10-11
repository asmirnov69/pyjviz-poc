#!/usr/bin/env python3

"""https://graphviz.org/Gallery/directed/fsm.html"""

import graphviz

f = graphviz.Digraph('finite_state_machine', filename='fsm.gv', format='png')
f.attr(rankdir='TB', size='8,5', splines = 'ortho')

f.attr('node', shape='doublecircle')
f.node('LR_0')
f.node('LR_3')
f.node('LR_4')
f.node('LR_8')

f.attr('node', shape='circle')
f.edge('LR_0', 'LR_2', xlabel='SS(B)')
f.edge('LR_0', 'LR_1', xlabel='SS(S)')
f.edge('LR_1', 'LR_3', xlabel='S($end)')
f.edge('LR_2', 'LR_6', xlabel='SS(b)')
f.edge('LR_2', 'LR_5', xlabel='SS(a)')
f.edge('LR_2', 'LR_4', xlabel='S(A)')
f.edge('LR_5', 'LR_7', xlabel='S(b)')
f.edge('LR_5', 'LR_5', xlabel='S(a)')
f.edge('LR_6', 'LR_6', xlabel='S(b)')
f.edge('LR_6', 'LR_5', xlabel='S(a)')
f.edge('LR_7', 'LR_8', xlabel='S(b)')
f.edge('LR_7', 'LR_5', xlabel='S(a)')
f.edge('LR_8', 'LR_6', xlabel='S(b)')
f.edge('LR_8', 'LR_5', xlabel='S(a)')

f.view()
