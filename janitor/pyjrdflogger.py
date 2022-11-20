# pyjrdf to keep all rdf logging functionality
#
import sys, threading
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

def get_curr_cmp_name__():
    thread_locals = threading.local()
    ret = None
    if hasattr(thread_locals, 'ChainedMethodPipe_curr_cmp_name'):
        ret = thread_locals.ChainedMethodPipe_curr_cmp_name
    return ret

class RDFLogger:
    @staticmethod
    def init(out_filename): 
        global register
        register.pandas_call_reporting_obj = RDFLogger(out_filename)
    
    def __init__(self, out_filename):        
        self.out_fd = open_pyjrdf_output__(out_filename)
        self.registered_dataframes = set()
        self.registered_dataframes_cmps = set() # (dfid, cmp)
        self.random_id = 0 # should be better way
        self.registered_cmps = {}

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

        curr_cmp_name = get_curr_cmp_name__()
        df_id_cmp = (id(df_ref), curr_cmp_name)
        if not df_id_cmp in self.registered_dataframes_cmps:
            self.registered_dataframes_cmps.add(df_id_cmp)
            cmp_uri = self.get_cmp_uri(curr_cmp_name)
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:cmp>", cmp_uri)
                
    def dump_pyj_method_call(self, df_this, method_name, method_args, df_ret):
        method_call_subj = f"<pyj:method:{self.random_id}>"; self.random_id += 1
        self.dump_triple(method_call_subj, "rdf:type", "<pyj:Method>")
        self.dump_triple(method_call_subj, "rdf:label", f'"{method_name}"')
        if get_curr_cmp_name__():
            self.dump_triple(method_call_subj, "<pyj:cmp>", self.get_cmp_uri(get_curr_cmp_name()))
        
        self.dump_triple(f"<pyj:{df_this}>", "<pyj:method-call>", method_call_subj)
        self.dump_triple(method_call_subj, "<pyj:method-return>", f"<pyj:{df_ret}>")

        for arg in method_args:
            if isinstance(arg, pd.DataFrame):
                self.register_dataframe(arg)
                self.dump_triple(f"<pyj:{id(arg)}>", "<pyj:method-call-arg>", method_call_subj)
    
    def dataframe_redirected_call(self, call_level, pandas_obj, method, *args, **kwargs):
        if call_level > 1:
            ret = method(pandas_obj, *args, **kwargs)
        else:
            self.register_dataframe(pandas_obj)
            ret = method(pandas_obj, *args, **kwargs)
            if id(ret) == id(pandas_obj):
                ret = pd.DataFrame(pandas_obj)
            self.register_dataframe(ret)
            self.dump_pyj_method_call(id(pandas_obj), method.__name__, args, id(ret))

        self.flush()
        
        return ret