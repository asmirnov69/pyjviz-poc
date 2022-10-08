import ipdb
import pandas as pd
#import pandas_flavor as pf
import janitor.register as pf

@pf.register_dataframe_method
def dropna(df: pd.DataFrame, axis = None, how = None) -> pd.DataFrame:
    print("my dropna")
    #return df.dropna(axis = axis, how = how)
    #ipdb.set_trace()
    return pf.old_dropna(df, axis = axis, how = how)

@pf.register_dataframe_method
def drop(df: pd.DataFrame, columns) -> pd.DataFrame:
    print("my drop")
    return pf.old_drop(df, columns = columns)
