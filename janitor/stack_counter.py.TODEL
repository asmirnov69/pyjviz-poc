#import ipdb

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
        

        
if __name__ == "__main__":
    def f(cc):
        with cc.get_sc() as sc:
            print(sc.scf.level)
            if sc.scf.level > 4:
                return
            f(cc)
    scf = SCF()
    #ipdb.set_trace()
    f(scf)
    
    
