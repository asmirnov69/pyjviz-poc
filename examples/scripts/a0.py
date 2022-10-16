#import ipdb
import os.path
import sys; sys.path.append("../..")

import typing
import pandas as pd

import janitor.register as register
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
    register.setup_pyjrdf_output(rdflog_fn)

    print(register.registered_methods)
    for rm_name, rm_anno in register.registered_methods.items():
        print(rm_name)
        print(rm_anno)
        for arg_n, arg_t in rm_anno.items():
            print(arg_n, arg_t)
            if isinstance(arg_t, typing.NewType):
                print("base class:", arg_t.__supertype__)

    #print(TestDF, TestDF.__name__, TestDF.__supertype__)
    #print(TestDF.columns)

    df = pd.DataFrame({'a': range(10)})
    df1 = df.a0()
    print(df1)
    
    pyjviz.render_rdflog(rdflog_fn)
