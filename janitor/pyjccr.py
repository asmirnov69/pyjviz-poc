"""
CCR - Chained Call Return. This is the term to desribe usual for pyjanitor (and many other tools and context) situation when subsequent calls of certain methods are done on previously returned object. Some people may even think about CCR as design pattern - I have exactly no opinion about that.

Consider an example from https://github.com/pyjanitor-devs/pyjanitor/blob/dev/examples/notebooks/dirty_data.ipynb cell 5:

   df_clean = (
      df
      .clean_names()
      .remove_empty()
      .rename_column("%_allocated", "percent_allocated")
      .rename_column("full_time_", "full_time")
   )

This is an example of CCR idea in use: each new method call of object df returns somthing which can be called by next method.

Proposed pyjanitor feature called CCR suppose to introduce similar notion with some important additions:

   df_clean = CCR("from_dirty_to_clean", lambda:
      df
      .clean_names()
      .remove_empty()
      .rename_column("%_allocated", "percent_allocated")
      .rename_column("full_time_", "full_time")
   )

CCR call result is identical to original example. It introduces name of CCR to be from_dirty_to_clean. This name can later be used to identify traces of exactly this CCR call.

"""



curr_ccr_name = "none"

def get_curr_ccr_name():
    return curr_ccr_name

def CCR(ccr_name, ccr_func):
    print("CCR start:", ccr_name)
    globals()['curr_ccr_name'] = ccr_name
    ret = ccr_func()
    print("ccr end:", ccr_name)
    return ret

