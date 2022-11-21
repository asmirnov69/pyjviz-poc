CMC - Chained Methods Call. This is the term to describe usual for pyjanitor (and many other tools and context) situation when subsequent calls of certain methods are done on previously returned object.

ChinedMethodsCall is implementation of an idea to introduce chain of method calls as  real object rather than language idiom. Chained methods call can viewed as another way to express function composition:
$$
a.m1().m2().m3() \leftrightarrow m3(m2(m1(a))) \leftrightarrow m1 \circ m2 \circ m3
$$

Consider an example from https://github.com/pyjanitor-devs/pyjanitor/blob/dev/examples/notebooks/dirty_data.ipynb cell 5:

```python
df_clean = (
df
.clean_names()
.remove_empty()
.rename_column("%_allocated", "percent_allocated")
.rename_column("full_time_", "full_time")
)
```

This is an example of CMC idea in use: each new method call of object df returns something which can be use for next method call ChainedMethodsCall [[tbc]] is to provide some additional functionality: it will same some additional rdf triples into program log: [[tbc]] **check can the code below survive copy/paste**

```python
df_clean_cmp = ChainedMethodsCall("from_dirty_to_clean", 
								  lambda: df \
									.clean_names()
									.remove_empty()
									.rename_column("%_allocated", "percent_allocated")
									.rename_column("full_time_", "full_time"))

df_clean = df_clean_cmp.run()
```

## Chained Methods Call - some details

CMC - chained methods call - term to designate used by pyj language construction of subsequent method calls where each next call uses return of previous one as first arg.

```python

# scetch

class ChainedMethodCall:

	def __init__(self, name, cmc_func):
		self.name = name
		self.cmc_func
		
	def run(self) -> DataFrame:
		print(“cmc starts”, self.name)
		ret = self.cmc_func()
		print(“cmc done”)
		return ret

	# Spawn func call on thread
	def async_run(self) -> None:
		self.call_thread = new_thread.call(self.cmc_func)
		return self

	#waits and returns once result available
	def wait(self) -> DataFrame:
		self.call_thread.wait()
		return self.call_thread.get_results()
	
	def call_cmc(name, pb):
		return ChainedMethodsCall(name, pb).run()

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
