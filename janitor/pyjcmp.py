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
r"""
## Chained Methods Pipe - some details

CMP - chained methods pipe - term to designate used by pyj language construction of subsequent method calls where each next call uses
return of previous one as first arg.


```python

# scetch

class ChainedMethodPipe:
      def __init__(self, name, cmp_func):
      	  self.name = name
	  self.cmp_func

      def run(self) -> DataFrame:
          print(“comps starts”, self.name)
	  ret = self.cmp_func()
          print(“cmp done”)
	  return ret

     # Spawn func call on thread
     def async_run(self) -> None:
         self.call_thread = new_thread.call(self.cmp_func)
         return self

     #waits and returns once result available
     def wait(self) -> DataFrame:
         self.call_thread.wait()
         return self.call_thread.get_results()

def call_cmp(name, pb):
    return ChainedMethodPipe(name, pb).run()
```


```python
# some usage examples:

df = ...
df1 = ...

res_df = df.fff().ggg(df1.hhh()).zzz()

res_df = call_cmp(“p1”, lambda: df.fff().ggg(call_cmp(“p2”, lambda: df1.hhh()).zzz())

df1_cmp = ChainedMethodCall(p2”, lambda: df1.hhh())
res_df = call_cmp(“p1”, lambda: df.fff().ggg(df1_cmp.run()).zzz())

# async call and wait
df1_cmp = ChainedMethodCall(“p2p2”, lambda: df1.hhh()).run_async()
res_df = call_cmp(“p1p”, lambda: df.fff().ggg(df1_cmp.wait()).zzz())

# fork

left_df, right_df = df1.aaa().fork("left", lambda x: x.left(), "right", lambda x: x.right())
call_cmp("left", lambda: left_df.ccc().join(call_cmp("right", right_df.ccc()))

```
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

