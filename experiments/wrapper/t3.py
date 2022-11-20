import ipdb
import ast, inspect, bytecode
import dis
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
    # pb.__code__ -- see also https://www.codeguage.com/courses/python/functions-code-objects
    # any chance to modify code to insert Wrapper as chain start? I.e. df should be replaced
    # with Wrapper(df)
    #
    # ipdb> pb.__code__.co_names
    # ('df', 'my_transform')
    # ipdb> pb.__code__.co_code
    # b't\x00\xa0\x01\xa1\x00S\x00'
    ipdb.set_trace()

    print(dis.dis(pb)) # show VM disassembly
    if 0:
        # unmodified call
        ret = pb()
    else:
        # bytecode module docs: https://bytecode.readthedocs.io/en/latest/usage.html
        instructions = bytecode.ConcreteBytecode.from_code(pb.__code__)
        print([x for x in instructions])
        # we can modify instructions here, see https://bytecode.readthedocs.io/en/latest/usage.html#concrete-bytecode
        pb.__code__ = bytecode.ConcreteBytecode.to_code(instructions)
        ret = pb()

    print("all done")
    return ret.d_o
    
def my_transform(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:3,:]

#register_spec_method(my_transform)
methods_d['my_transform'] = my_transform



df = pd.DataFrame({'a': range(10)})
if 1:
    # note that we need to use Wrapper to start the chain
    ret = call_cmp("test-pipe", lambda: Wrapper(df).my_transform())
else:
    # experiment: could we insert Wrapper(df) instead of df into lambda function
    # using func described here https://www.codeguage.com/courses/python/functions-code-objects
    ret = call_cmp("test-pipe", lambda: df.my_transform())
print(ret)



