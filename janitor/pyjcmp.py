"""
CMP - Chained Methods Call. This is the term to desribe usual for pyjanitor (and many other tools and context) situation when subsequent calls of certain methods are done on previously returned object.

Consider an example from https://github.com/pyjanitor-devs/pyjanitor/blob/dev/examples/notebooks/dirty_data.ipynb cell 5:

   df_clean = (
      df
      .clean_names()
      .remove_empty()
      .rename_column("%_allocated", "percent_allocated")
      .rename_column("full_time_", "full_time")
   )

This is an example of CMP idea in use: each new method call of object df returns something which can be use for next method call

ChainedMethodsPipe is to provide some additional functionality: it will same some additional rdf triples into program log:

   df_clean_cmp = ChainedMethodsPipe("from_dirty_to_clean", lambda:
      df
      .clean_names()
      .remove_empty()
      .rename_column("%_allocated", "percent_allocated")
      .rename_column("full_time_", "full_time")
   )

   df_clean = df_clean_cmp.run()

"""

curr_cmp_name = "none"

def get_curr_cmp_name():
    return curr_cmp_name

class ChainedMethodsPipe:
    def __init__(self, name, cmp_func):
        self.name = name
        self.cmp_func = cmp_func

    def run(self):
        print("CMP start:", self.name)
        globals()['curr_cmp_name'] = self.name
        ret = self.cmp_func()
        print("cmp end:", self.name)
        return ret
        
def call_cmp(cmp_name, cmp_func):
    return ChainedMethodsPipe(cmp_name, cmp_func).run()

