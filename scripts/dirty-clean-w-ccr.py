#
# CCR added to the first example from https://github.com/samukweku/pyjanitor_presentation/blob/main/janitor/pyjanitor_PyData_Sydney.ipynb
#

import sys; sys.path.append("..")

import pandas as pd

import janitor.register as register
from janitor.functions import *
import janitor.pyjccr as pyjccr

if __name__ == "__main__":
    # configure pyjrdf
    register.setup_pyjrdf_output("./rdflog.ttl")
    
    if 0:
        url = "https://github.com/pyjanitor-devs/pyjanitor/blob/dev/examples/notebooks/dirty_data.xlsx?raw=true"
        dirty = pd.read_excel(url, engine = 'openpyxl')        
    else:
        dirty = pd.read_excel("../data/dirty_data.xlsx")
        
    #print(dirty)    

    clean = pyjccr.CCR("from_dirty_to_clean", lambda:
                       dirty.clean_names()
                       .dropna(axis='columns', how='all')
                       .dropna(axis='rows', how='all')
                       .rename(columns={"%_allocated": "percent_allocated", "full_time_": "full_time"})
                       .assign(certification = lambda df: df.certification.combine_first(df.certification_1))
                       .drop(columns='certification_1')
                       .assign(hire_date = lambda df: pd.to_datetime(df.hire_date, unit='D', origin='1899-12-30'))
                       )
    print(clean)
    
