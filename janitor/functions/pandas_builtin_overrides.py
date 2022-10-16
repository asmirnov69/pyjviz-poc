#import ipdb
import pandas as pd
#import pandas_flavor as pf
import janitor.register as pf

# replaces own pandas methods with janitor, drop gives only warning
old_dropna = pd.DataFrame.dropna; del pd.DataFrame.dropna
old_drop = pd.DataFrame.drop; del pd.DataFrame.drop
old_rename = pd.DataFrame.rename; del pd.DataFrame.rename
old_assign = pd.DataFrame.assign; del pd.DataFrame.assign

@pf.register_dataframe_method
def dropna(df: pd.DataFrame, axis = None, how = None) -> pd.DataFrame:
    ret = old_dropna(df, axis = axis, how = how)
    #print("my dropna", id(df), id(ret))
    return ret
    
@pf.register_dataframe_method
def drop(df: pd.DataFrame, columns) -> pd.DataFrame:
    ret = old_drop(df, columns = columns)
    #print("my drop", id(df), id(ret))
    return ret

@pf.register_dataframe_method
def rename(df: pd.DataFrame, columns) -> pd.DataFrame:
    ret = old_rename(df, columns = columns)
    #print("my rename", id(df), id(ret))
    return ret
    
@pf.register_dataframe_method
def assign(df: pd.DataFrame, **kw) -> pd.DataFrame:
    ret = old_assign(df, **kw)
    #print("my assign", id(df), id(ret))
    return ret

