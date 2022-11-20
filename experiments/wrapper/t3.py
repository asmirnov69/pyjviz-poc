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

def call_cmp(mod_code, name, pb):
    print("calling pipe", name)
    print(dis.dis(pb)) # show VM disassembly

    ipdb.set_trace()
    if mod_code == False:
        # unmodified call
        ret = pb()
    else:
        # bytecode module docs: https://bytecode.readthedocs.io/en/latest/usage.html
        instructions = bytecode.ConcreteBytecode.from_code(pb.__code__)
        print([x for x in instructions])
        # we can modify instructions here, see https://bytecode.readthedocs.io/en/latest/usage.html#concrete-bytecode
        instructions.names.append('Wrapper') # appending Wrapper to names to avoid arg shift in exisiting bytecode
        instructions.insert(0, bytecode.ConcreteInstr('LOAD_GLOBAL', len(instructions.names) - 1))
        instructions.insert(2, bytecode.ConcreteInstr('CALL_FUNCTION', 1))
        
        pb.__code__ = bytecode.ConcreteBytecode.to_code(instructions)
        print("modified code:")
        print(dis.dis(pb)) # show VM disassembly
        ret = pb()

    print("all done")
    return ret.d_o
    
def my_transform(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:3,:]

#register_spec_method(my_transform)
methods_d['my_transform'] = my_transform


if __name__ == "__main__":
    df = pd.DataFrame({'a': range(10)})
    if 1:
        # note that we need to use Wrapper to start the chain
        ret = call_cmp(False, "test-pipe", lambda: Wrapper(df).my_transform())
        print(ret)
        
    print("-------------")
    if 1:
        # experiment: could we insert Wrapper(df) instead of df into lambda function
        # using func described here https://www.codeguage.com/courses/python/functions-code-objects
        ret = call_cmp(True, "test-pipe", lambda: df.my_transform())
        print(ret)

