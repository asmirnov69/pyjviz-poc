#import ipdb

class Dest:
    def do_it_in_dest(self, a, b, c):
        print("Dest called:", a, b, c)
        return "hi"
        
    def another_call(self):
        print("another call")

class CallWrapper:
    def __init__(self, bound_method):
        self.bound_method = bound_method

    def __call__(self, *args):
        print("__call__")
        ret = self.bound_method(*args)
        print("__call__ ret:", type(ret))
        return ret
        
class Wrapper:
    def __init__(self, d_o):
        self.d_o = d_o

    def __getattr__(self, attr):
        #ipdb.set_trace()
        d_o = self.__getattribute__('d_o')
        d_o_m = d_o.__getattribute__(attr)
        return CallWrapper(d_o_m)


d = Dest()
w = Wrapper(d)
print(w.do_it_in_dest('Hello', ',', 'world'))
w.another_call()

