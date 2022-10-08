import random, string
from functools import wraps
import pandas as pd
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor

# replaces own pandas methods with janitor
old_drop_na = pd.DataFrame.dropna; del pd.DataFrame.dropna

def get_new_node_label(node_label):
    if node_label and '-' in node_label:
        new_node_label = node_label.split('-')[0]
    else:
        new_node_label = 'new'        
    return new_node_label + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


registered_methods = {}

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
                if not 'label' in self._obj.attrs:
                    self._obj.attrs['label'] = get_new_node_label(None)

                obj_label = self._obj.attrs.get('label')

                arg1_label = None
                for i in range(len(args)):
                    print(type(args[i]))
                    if isinstance(args[i], pd.DataFrame):
                        if not 'label' in args[i].attrs:
                            arg1_label = get_new_node_label(None)
                        else:
                            arg1_label = args[i].attrs.get('label')
                print("------")

                ret = method(self._obj, *args, **kwargs)
                
                ret_label = get_new_node_label(obj_label)
                print("s p o:", obj_label, method.__name__, ret_label)
                if not arg1_label is None:
                    print("args s p o:", arg1_label, method.__name__, ret_label)
                            
                #print("s p o:", id(self._obj), method.__name__, id(ret))
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
