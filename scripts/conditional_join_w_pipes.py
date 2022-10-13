#
# example https://github.com/pyjanitor-devs/pyjanitor/blob/dev/examples/notebooks/conditional_join.ipynb
#

import sys; sys.path.append("..")

import pandas as pd

import janitor.register as register
from janitor.functions import *
import janitor.pyjpipe as pyjpipe

if __name__ == "__main__":
    # configure pyjrdf
    register.setup_pyjrdf_output("./rdflog.ttl")

    df1 = pd.DataFrame({'id': [1,1,1,2,2,3],
                        'value_1': [2,5,7,1,3,4]})

    df2 = pd.DataFrame({'id': [1,1,1,1,2,2,2,3],
                        'value_2A': [0,3,7,12,0,2,3,1],
                        'value_2B': [1,5,9,15,1,4,6,3]})


    if 1:
        res1 = pyjpipe.pipe("p1",
                            lambda: df1.conditional_join(df2,
                                                         ('id', 'id', "<"),
                                                         df_columns = {'id':'df_id'},
                                                         right_columns = {'id':'right_id'}
                                                         ))
        print(res1)

    if 1:
        res2 = pyjpipe.pipe("p2",
                            lambda: df1.select_columns('value_1').conditional_join(
                                df2.select_columns('val*'),
                                ('value_1', 'value_2A', '>'),
                            ('value_1', 'value_2B', '<'),
                            ))
        print(res2)
