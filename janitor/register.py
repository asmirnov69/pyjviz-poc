# the code in this file is based on https://github.com/Zsailer/pandas_flavor/blob/master/pandas_flavor/register.py
#
from functools import wraps
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor

import warnings
warnings.filterwarnings("ignore", category = UserWarning)

class StackCounter:
    def __init__(self, scf):
        self.scf = scf
        
    def __enter__(self):
        #print("StackCounter:__enter__", id(self))
        self.scf.level += 1
        return self

    def __exit__(self, type, value, traceback):
        #print("StackCounter:__exit__", id(self))
        self.scf.level -= 1
        
class SCF:
    def __init__(self):
        self.level = 0
        
    def get_sc(self):
        return StackCounter(self)

global_scf = SCF()
pandas_call_reporting_obj = None

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

            # this method was modified to collect enough infomation about the call
            # to pass that to pyjrdf method calls which responsible for rdf triple dumping to rdf log file
            @wraps(method)
            def __call__(self, *args, **kwargs):                
                global pandas_call_reporting_obj
                if pandas_call_reporting_obj:
                    with global_scf.get_sc() as sc:
                        return pandas_call_reporting_obj.dataframe_redirected_call(sc.scf.level, self._obj, method, *args, **kwargs)

        # this is location where pandas.api.extensions used to register method caller class
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
