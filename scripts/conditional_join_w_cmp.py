#
# example https://github.com/pyjanitor-devs/pyjanitor/blob/dev/examples/notebooks/conditional_join.ipynb
#

import sys; sys.path.append("..")

import pandas as pd

import janitor.pyjviz as pyjviz
from janitor.pyjrdflogger import RDFLogger
from janitor.pyjrdflogger import call_cmp

from janitor.functions import *

if __name__ == "__main__":
    # configure pyjrdf
    rdflog_fn = pyjviz.get_rdflog_filename(sys.argv[0])
    RDFLogger.init(rdflog_fn)
    
    df1 = pd.DataFrame({'id': [1,1,1,2,2,3],
                        'value_1': [2,5,7,1,3,4]})

    df2 = pd.DataFrame({'id': [1,1,1,1,2,2,2,3],
                        'value_2A': [0,3,7,12,0,2,3,1],
                        'value_2B': [1,5,9,15,1,4,6,3]})


    if 1:
        res1 = call_cmp("p1",
                        lambda: df1.conditional_join(df2,
                                                     ('id', 'id', "<"),
                                                     df_columns = {'id':'df_id'},
                                                     right_columns = {'id':'right_id'}
                                                     ))
        print(res1)

    if 1:
        res2 = call_cmp("p2",
                        lambda: df1.select_columns('value_1').conditional_join(
                            df2.select_columns('val*'),
                            ('value_1', 'value_2A', '>'),
                            ('value_1', 'value_2B', '<'),
                        ))
        print(res2)

    pyjviz.render_rdflog(rdflog_fn)
    
