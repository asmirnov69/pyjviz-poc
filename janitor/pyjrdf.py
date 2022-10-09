import sys

class pyjrdf:
    def __init__(self, out_fd):
        self.out_fd = out_fd
        
    def dump_pyj_method_call(self, df_actor, method_name, df_result):
        subj = f"pyjpoc:{df_actor}"
        pred = f"pyjpoc:{method_name}"
        obj = f"pyjpoc:{df_result}"
        print(subj, pred, obj, ".", file = self.out_fd)
    
    

