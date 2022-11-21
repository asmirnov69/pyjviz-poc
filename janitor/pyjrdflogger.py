# pyjrdf to keep all rdf logging functionality
#
import sys
import os.path
import pandas as pd

import janitor.register as register

def open_pyjrdf_output__(out_fn):
    out_dir = os.path.dirname(out_fn)    
    if out_dir != "" and not os.path.exists(out_dir):
        print("setup_pyjrdf_output:", out_dir)
        os.makedirs(out_dir)
    out_fd = open(out_fn, "wt")

    # rdf prefixes used by PYJRDFLogger
    print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", file = out_fd)
    
    return out_fd

ChainedMethodsCall_curr_cmc_name = None
def get_curr_cmc_name__():
    ret = "none"
    global ChainedMethodsCall_curr_cmc_name    
    if ChainedMethodsCall_curr_cmc_name:
        ret = ChainedMethodsCall_curr_cmc_name
    return ret

class ChainedMethodsCall:
    def __init__(self, name, cmc_func):
        self.name = name
        self.cmc_func = cmc_func

    def run(self):
        print("CMC start:", self.name)
        global ChainedMethodsCall_curr_cmc_name
        ChainedMethodsPipe_curr_cmc_name = self.name
        ret = self.cmc_func()
        print("cmc end:", self.name)
        return ret
        
def call_cmc(cmc_name, cmc_func):
    return ChainedMethodsCall(cmc_name, cmc_func).run()


class RDFLogger:
    @staticmethod
    def init(out_filename): 
        global register
        register.pandas_call_reporting_obj = RDFLogger(out_filename)
    
    def __init__(self, out_filename):        
        self.out_fd = open_pyjrdf_output__(out_filename)
        self.known_dataframes = set()
        self.known_dataframes_cmps = set() # (dfid, cmp)
        self.random_id = 0 # should be better way
        self.known_cmps = {}

    def flush__(self):
        self.out_fd.flush()
        
    def dump_triple__(self, subj, pred, obj):
        print(subj, pred, obj, ".", file = self.out_fd)

    def get_cmp_uri__(self, cmp_name):
        if not cmp_name in self.known_cmps:
            cmp_uri = f"<pyj:cmp:{self.random_id}>"; self.random_id += 1
            self.known_cmps[cmp_name] = cmp_uri            
            self.dump_triple__(cmp_uri, "rdf:type", "<pyj:CMP>")
            self.dump_triple__(cmp_uri, "rdf:label", f'"{cmp_name}"')
        return self.known_cmps.get(cmp_name)
        
    def remember_dataframe__(self, df_ref):
        if not id(df_ref) in self.known_dataframes:
            self.known_dataframes.add(id(df_ref))
            self.dump_triple__(f"<pyj:{id(df_ref)}>", "rdf:type", "<pyj:DataFrame>")
            self.dump_triple__(f"<pyj:{id(df_ref)}>", "<pyj:df-shape>", f'"{df_ref.shape}"')
            #ipdb.set_trace()
            self.dump_triple__(f"<pyj:{id(df_ref)}>", "<pyj:df-columns>", '"' + f"{','.join(df_ref.columns)}" + '"')

        curr_cmp_name = get_curr_cmc_name__()
        df_id_cmp = (id(df_ref), curr_cmp_name)
        if not df_id_cmp in self.known_dataframes_cmps:
            self.known_dataframes_cmps.add(df_id_cmp)
            cmp_uri = self.get_cmp_uri__(curr_cmp_name)
            self.dump_triple__(f"<pyj:{id(df_ref)}>", "<pyj:cmp>", cmp_uri)
                
    def dump_pyj_method_call__(self, df_this, method_name, method_args, df_ret):
        method_call_subj = f"<pyj:method:{self.random_id}>"; self.random_id += 1
        self.dump_triple__(method_call_subj, "rdf:type", "<pyj:Method>")
        self.dump_triple__(method_call_subj, "rdf:label", f'"{method_name}"')
        self.dump_triple__(method_call_subj, "<pyj:cmp>", self.get_cmp_uri__(get_curr_cmc_name__()))
        
        self.dump_triple__(f"<pyj:{df_this}>", "<pyj:method-call>", method_call_subj)
        self.dump_triple__(method_call_subj, "<pyj:method-return>", f"<pyj:{df_ret}>")

        for arg in method_args:
            if isinstance(arg, pd.DataFrame):
                self.remember_dataframe__(arg)
                self.dump_triple__(f"<pyj:{id(arg)}>", "<pyj:method-call-arg>", method_call_subj)
    
    def handle_dataframe_method_call(self, method_return_obj, pandas_obj, method, *args, **kwargs):
        self.remember_dataframe__(pandas_obj)
        self.remember_dataframe__(method_return_obj)
        self.dump_pyj_method_call__(id(pandas_obj), method.__name__, args, id(method_return_obj))
        self.flush__()
