#import ipdb
import os.path
import sys; sys.path.append("..")

import typing
import pandas as pd

import janitor.register as register
import janitor.pyjrdf as pyjrdf
import janitor.pyjviz as pyjviz

TestDF = typing.NewType('TestDF', pd.DataFrame)
TestDF.columns = ['a']

@register.register_dataframe_method
def a0(df: pd.DataFrame) -> TestDF:
    print("a0")
    return df

if __name__ == "__main__":
    # configure pyjrdf
    rdflog_fn = pyjviz.get_rdflog_filename(sys.argv[0])
    pyjrdf.PYJRDF.init(rdflog_fn)

    print(TestDF, TestDF.__name__, TestDF.__supertype__)
    print(TestDF.columns)

    df = pd.DataFrame({'a': range(10)})
    df1 = df.a0()
    print(df1)
    
    pyjviz.render_rdflog(rdflog_fn)
