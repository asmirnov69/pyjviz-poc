import sys

class pyjrdf:
    def __init__(self, out_fd):
        self.out_fd = out_fd

    def dump_triple(self, subj, pred, obj):
        print(subj, pred, obj, ".", file = self.out_fd)
        
    def dump_pyj_method_call(self, df_actor, method_name, df_result):
        subj = df_actor
        pred = method_name
        obj = df_result
        self.dump_triple(subj, pred, obj)
    

