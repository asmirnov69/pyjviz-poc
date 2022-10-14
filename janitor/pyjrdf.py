import sys
import pandas as pd
from .pyjccr import *

class pyjrdf:
    def __init__(self, out_fd):
        self.out_fd = out_fd
        self.registered_dataframes = set()
        self.registered_dataframes_ccrs = set() # (dfid, ccr)
        self.random_id = 0 # should be better way
        self.registered_ccrs = {}

        print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", file = out_fd)

    def flush(self):
        self.out_fd.flush()
        
    def dump_triple(self, subj, pred, obj):
        print(subj, pred, obj, ".", file = self.out_fd)

    def get_ccr_uri(self, ccr_name):
        if not ccr_name in self.registered_ccrs:
            ccr_uri = f"<pyj:ccr:{self.random_id}>"; self.random_id += 1
            self.registered_ccrs[ccr_name] = ccr_uri            
            self.dump_triple(ccr_uri, "rdf:type", "<pyj:CCR>")
            self.dump_triple(ccr_uri, "rdf:label", f'"{ccr_name}"')
        return self.registered_ccrs.get(ccr_name)
        
    def register_dataframe(self, df_ref):
        if not id(df_ref) in self.registered_dataframes:
            self.registered_dataframes.add(id(df_ref))
            self.dump_triple(f"<pyj:{id(df_ref)}>", "rdf:type", "<pyj:DataFrame>")
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:df-shape>", f'"{df_ref.shape}"')
            #ipdb.set_trace()
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:df-columns>", '"' + f"{','.join(df_ref.columns)}" + '"')

        curr_ccr_name = get_curr_ccr_name()
        df_id_ccr = (id(df_ref), curr_ccr_name)
        if not df_id_ccr in self.registered_dataframes_ccrs:
            self.registered_dataframes_ccrs.add(df_id_ccr)
            ccr_uri = self.get_ccr_uri(curr_ccr_name)
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:ccr>", ccr_uri)
                
    def dump_pyj_method_call(self, df_this, method_name, method_args, df_ret):
        method_call_subj = f"<pyj:method:{self.random_id}>"; self.random_id += 1
        self.dump_triple(method_call_subj, "rdf:type", "<pyj:Method>")
        self.dump_triple(method_call_subj, "rdf:label", f'"{method_name}"')
        if get_curr_ccr_name():
            self.dump_triple(method_call_subj, "<pyj:ccr>", self.get_ccr_uri(get_curr_ccr_name()))
        
        self.dump_triple(f"<pyj:{df_this}>", "<pyj:method-call>", method_call_subj)
        self.dump_triple(method_call_subj, "<pyj:method-return>", f"<pyj:{df_ret}>")

        for arg in method_args:
            if isinstance(arg, pd.DataFrame):
                self.register_dataframe(arg)
                self.dump_triple(f"<pyj:{id(arg)}>", "<pyj:method-call-arg>", method_call_subj)
    

