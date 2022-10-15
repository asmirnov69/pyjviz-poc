import sys
import pandas as pd
from .pyjcmp import *

class pyjrdf:
    def __init__(self, out_fd):
        self.out_fd = out_fd
        self.registered_dataframes = set()
        self.registered_dataframes_cmps = set() # (dfid, cmp)
        self.random_id = 0 # should be better way
        self.registered_cmps = {}

        print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", file = out_fd)

    def flush(self):
        self.out_fd.flush()
        
    def dump_triple(self, subj, pred, obj):
        print(subj, pred, obj, ".", file = self.out_fd)

    def get_cmp_uri(self, cmp_name):
        if not cmp_name in self.registered_cmps:
            cmp_uri = f"<pyj:cmp:{self.random_id}>"; self.random_id += 1
            self.registered_cmps[cmp_name] = cmp_uri            
            self.dump_triple(cmp_uri, "rdf:type", "<pyj:CMP>")
            self.dump_triple(cmp_uri, "rdf:label", f'"{cmp_name}"')
        return self.registered_cmps.get(cmp_name)
        
    def register_dataframe(self, df_ref):
        if not id(df_ref) in self.registered_dataframes:
            self.registered_dataframes.add(id(df_ref))
            self.dump_triple(f"<pyj:{id(df_ref)}>", "rdf:type", "<pyj:DataFrame>")
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:df-shape>", f'"{df_ref.shape}"')
            #ipdb.set_trace()
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:df-columns>", '"' + f"{','.join(df_ref.columns)}" + '"')

        curr_cmp_name = get_curr_cmp_name()
        df_id_cmp = (id(df_ref), curr_cmp_name)
        if not df_id_cmp in self.registered_dataframes_cmps:
            self.registered_dataframes_cmps.add(df_id_cmp)
            cmp_uri = self.get_cmp_uri(curr_cmp_name)
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:cmp>", cmp_uri)
                
    def dump_pyj_method_call(self, df_this, method_name, method_args, df_ret):
        method_call_subj = f"<pyj:method:{self.random_id}>"; self.random_id += 1
        self.dump_triple(method_call_subj, "rdf:type", "<pyj:Method>")
        self.dump_triple(method_call_subj, "rdf:label", f'"{method_name}"')
        if get_curr_cmp_name():
            self.dump_triple(method_call_subj, "<pyj:cmp>", self.get_cmp_uri(get_curr_cmp_name()))
        
        self.dump_triple(f"<pyj:{df_this}>", "<pyj:method-call>", method_call_subj)
        self.dump_triple(method_call_subj, "<pyj:method-return>", f"<pyj:{df_ret}>")

        for arg in method_args:
            if isinstance(arg, pd.DataFrame):
                self.register_dataframe(arg)
                self.dump_triple(f"<pyj:{id(arg)}>", "<pyj:method-call-arg>", method_call_subj)
    

