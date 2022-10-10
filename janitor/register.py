import ipdb
import inspect
import random, string
from functools import wraps
import pandas as pd
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor

import janitor.pyjrdf as pyjrdf_mod
import janitor.stack_counter as stack_counter

pyjrdf = None
def setup_pyjrdf_output(out_fn):
    out_fd = open(out_fn, "wt")
    globals()['pyjrdf'] = pyjrdf_mod.pyjrdf(out_fd)

def get_new_node_label(node_label):
    if node_label and '-' in node_label:
        new_node_label = node_label.split('-')[0]
    else:
        new_node_label = 'new'        
    return new_node_label + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

registered_methods = {}
global_scf = stack_counter.SCF()

def register_dataframe_method(method):
    """Register a function as a method attached to the Pandas DataFrame.

    Example
    -------

    .. code-block:: python

        @register_dataframe_method
        def print_column(df, col):
            '''Print the dataframe column given'''
            print(df[col])
    """

    def inner(*args, **kwargs):
        class AccessorMethod(object):
            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                if not 'pipe_first' in self._obj.attrs:
                    #ipdb.set_trace()
                    print(f"no pipe_first attr for df {id(self._obj)}, setting up new one")
                    self._obj.attrs['pipe_first'] = id(self._obj)

                pipe_first = self._obj.attrs['pipe_first']
                with global_scf.get_sc() as sc:
                    #print("sc level:", sc.scf.level)
                    if sc.scf.level > 1:
                        ret = method(self._obj, *args, **kwargs)
                    else:
                        pipe_this = id(self._obj)

                        arg1_df = None
                        for aa in args:
                            print(type(aa))
                            if isinstance(aa, pd.DataFrame):
                                arg1_df = aa
                                break

                        ret = method(self._obj, *args, **kwargs)
                        if id(ret) == id(self._obj):
                            print("new to create new id:", id(self._obj), id(ret))
                            ret = pd.DataFrame(self._obj)
                            print("new id:", id(ret))

                        if sc.scf.level == 1:
                            #ipdb.set_trace()
                            pyjrdf.dump_triple(f"<pyj:{pipe_this}>", "<pyj:pipe_head>", f"<pyj:{pipe_first}>")
                            pyjrdf.dump_pyj_method_call(f"<pyj:{pipe_this}>", f"<pyj:{method.__name__}>", f"<pyj:{id(ret)}>")
                            if not arg1_df is None:
                                pyjrdf.dump_pyj_method_call(f"<pyj:{id(arg1_df)}>", f"<pyj:{method.__name__}>", f"<pyj:{id(ret)}>")

                    if not 'pipe_first' in ret.attrs:
                        print(f"return pipe dataframe {id(ret)} without pipe_first attr, setting up and continue")
                        ret.attrs['pipe_first'] = pipe_first

                        
                    return ret
                
        registered_methods[method.__name__] = method.__annotations__
        register_dataframe_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_series_method(method):
    """Register a function as a method attached to the Pandas Series."""

    def inner(*args, **kwargs):
        class AccessorMethod(object):
            __doc__ = method.__doc__

            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                return method(self._obj, *args, **kwargs)

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
