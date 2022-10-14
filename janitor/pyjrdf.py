import sys
import pandas as pd
from .pyjpipe import *

class pyjrdf:
    def __init__(self, out_fd):
        self.out_fd = out_fd
        self.registered_dataframes = set()
        self.registered_dataframes_pipes = set() # (dfid, pipe)
        self.random_id = 0 # should be better way
        self.registered_pipes = {}

        print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", file = out_fd)

    def flush(self):
        self.out_fd.flush()
        
    def dump_triple(self, subj, pred, obj):
        print(subj, pred, obj, ".", file = self.out_fd)

    def get_pipe_uri(self, pipe_name):
        if not pipe_name in self.registered_pipes:
            pipe_uri = f"<pyj:pipe:{self.random_id}>"; self.random_id += 1
            self.registered_pipes[pipe_name] = pipe_uri            
            self.dump_triple(pipe_uri, "rdf:type", "<pyj:Pipe>")
            self.dump_triple(pipe_uri, "rdf:label", f'"{pipe_name}"')
        return self.registered_pipes.get(pipe_name)
        
    def register_dataframe(self, df_ref):
        if not id(df_ref) in self.registered_dataframes:
            self.registered_dataframes.add(id(df_ref))
            self.dump_triple(f"<pyj:{id(df_ref)}>", "rdf:type", "<pyj:DataFrame>")
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:df-shape>", f'"{df_ref.shape}"')
            #ipdb.set_trace()
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:df-columns>", '"' + f"{','.join(df_ref.columns)}" + '"')

        curr_pipe_name = get_curr_pipe_name()
        df_id_pipe = (id(df_ref), curr_pipe_name)
        if not df_id_pipe in self.registered_dataframes_pipes:
            self.registered_dataframes_pipes.add(df_id_pipe)
            pipe_uri = self.get_pipe_uri(curr_pipe_name)
            self.dump_triple(f"<pyj:{id(df_ref)}>", "<pyj:pipe>", pipe_uri)
                
    def dump_pyj_method_call(self, df_this, method_name, method_args, df_ret):
        method_call_subj = f"<pyj:method:{self.random_id}>"; self.random_id += 1
        self.dump_triple(method_call_subj, "rdf:type", "<pyj:Method>")
        self.dump_triple(method_call_subj, "rdf:label", f'"{method_name}"')
        if get_curr_pipe_name():
            self.dump_triple(method_call_subj, "<pyj:pipe>", self.get_pipe_uri(get_curr_pipe_name()))
        
        self.dump_triple(f"<pyj:{df_this}>", "<pyj:method-call>", method_call_subj)
        self.dump_triple(method_call_subj, "<pyj:method-return>", f"<pyj:{df_ret}>")

        for arg in method_args:
            if isinstance(arg, pd.DataFrame):
                self.register_dataframe(arg)
                self.dump_triple(f"<pyj:{id(arg)}>", "<pyj:method-call-arg>", method_call_subj)
    

