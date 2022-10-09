import ipdb
import pandas as pd
#import pandas_flavor as pf
import janitor.register as pf

# replaces own pandas methods with janitor
old_drop = pd.DataFrame.drop; del pd.DataFrame.drop
old_dropna = pd.DataFrame.dropna; del pd.DataFrame.dropna
old_rename = pd.DataFrame.rename; del pd.DataFrame.rename
old_assign = pd.DataFrame.assign; del pd.DataFrame.assign

@pf.register_dataframe_method
def dropna(df: pd.DataFrame, axis = None, how = None) -> pd.DataFrame:
    print("my dropna")
    return old_dropna(df, axis = axis, how = how)

@pf.register_dataframe_method
def drop(df: pd.DataFrame, columns) -> pd.DataFrame:
    print("my drop")
    return old_drop(df, columns = columns)

@pf.register_dataframe_method
def rename(df: pd.DataFrame, columns) -> pd.DataFrame:
    print("my rename")
    return old_rename(df, columns = columns)

@pf.register_dataframe_method
def assign(df: pd.DataFrame, **kw) -> pd.DataFrame:
    print("my assign")
    return old_assign(df, **kw)


