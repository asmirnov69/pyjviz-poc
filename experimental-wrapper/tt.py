#import ipdb
import pandas as pd

class CallWrapper:
    def __init__(self, o, method_o):
        self.o = o
        self.method_o = method_o

    def __call__(self, *args):
        print("__call__")
        ret = self.method_o(self.o, *args)
        print("__call__ ret:", type(ret))
        return Wrapper(ret)

methods_d = {}
    
class Wrapper:
    def __init__(self, d_o):
        self.d_o = d_o

    def __getattr__(self, attr):
        #ipdb.set_trace()
        d_o = self.__getattribute__('d_o')
        method_o = methods_d.get(attr)
        return CallWrapper(d_o, method_o)

def call_cmp(name, pb):
    print("calling pipe", name)
    ret = pb()
    print("all done")
    return ret.d_o
    
def my_transform(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:3,:]

#register_spec_method(my_transform)
methods_d['my_transform'] = my_transform



df = pd.DataFrame({'a': range(10)})
ret = call_cmp("test-pipe", lambda: Wrapper(df).my_transform())
#ret = call_cmp("test-pipe", lambda: df.my_transform())
print(ret)



