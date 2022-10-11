import sys
import pandas as pd

class pyjrdf:
    def __init__(self, out_fd):
        self.out_fd = out_fd
        self.registered_dataframes = set()
        self.random_id = 0 # should be better way

        print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", file = out_fd)
        
    def dump_triple(self, subj, pred, obj):
        print(subj, pred, obj, ".", file = self.out_fd)
        
    def register_dataframe(self, df_ref):
        if not id(df_ref) in self.registered_dataframes:
            self.registered_dataframes.add(id(df_ref))
            self.dump_triple(f"<pyj:{id(df_ref)}>", "rdf:type", "<pyj:DataFrame>")
                
    def dump_pyj_method_call(self, df_this, method_name, method_args, df_ret):
        method_call_subj = f"<pyj:method:{self.random_id}>"; self.random_id += 1
        self.dump_triple(method_call_subj, "rdf:type", "<pyj:Method>")
        self.dump_triple(method_call_subj, "rdf:label", f'"{method_name}"')

        self.dump_triple(f"<pyj:{df_this}>", "<pyj:method-call>", method_call_subj)
        self.dump_triple(method_call_subj, "<pyj:method-return>", f"<pyj:{df_ret}>")

        for arg in method_args:
            if isinstance(arg, pd.DataFrame):
                self.register_dataframe(arg)
                self.dump_triple(f"<pyj:{id(arg)}>", "<pyj:method-call-arg>", method_call_subj)
    

