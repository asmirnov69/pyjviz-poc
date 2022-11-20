
# register.py

^b0ef10

[pyjviz-poc/janitor/register.py](https://github.com/asmirnov69/pyjviz-poc/blob/main/janitor/register.py) is modified from [original version](https://github.com/Zsailer/pandas_flavor/blob/master/pandas_flavor/register.py) used by pyjanitor via import of [pandas_flavor](https://github.com/Zsailer/pandas_flavor) module

Most important change is in *`__call__`*  method of class *AccessorMethod*. Since that method intercepts all calls made during method chain call it is possible to insert neccessary code to keep track of all execution flow information. POC code uses global object *pyjrdf* to keep track of creation of new dataframes and putting [[RDF]] corresponding to the operation into rdf log. It saves infromation like called method name, arguments and id of dataframes.

# pyjrdf.py

[pyjviz-poc/janitor/pyjrdf.py](https://github.com/asmirnov69/pyjviz-poc/blob/main/janitor/pyjrdf.py) is module with main responsibility to provide conveniece methods to dump [[RDF]]. All that dump_* methods are suppose to be called by AccessorMethod object from [[#^b0ef10|register.py]]

# pyjcmp.py

[pyjviz-poc/janitor/pyjcmp.py](https://github.com/asmirnov69/pyjviz-poc/blob/main/janitor/pyjcmp.py) is implemenation of an idea to introduce chained methods pipe as   
real object rather than language idiom.
Chained method pipe looks like another way to express function composition:
$$
a.m1().m2().m3() \leftrightarrow m3(m2(m1(a))) \leftrightarrow m1 \circ m2 \circ m3
$$
Class *ChainedMethodPipe* defined in pyjcmp.py is just a wrapper which can be used along with another language idiom: lambda with empty argument list. It creates convenient syntax:

```python
res = a.m1().m2().m3() # chained method pipe
...
method_pipe = ChainedMethodPipe("m123 calls", lambda: a.m1().m2().m3())
res = method_pipe.run() # the same as a.m1().m2().m3()
```

Also ChainedMethodPipe class implementation can be used to place addition information to rdf log

# pyjviz.py

[pyjviz-poc/janitor/pyjviz.py](https://github.com/asmirnov69/pyjviz-poc/blob/main/janitor/pyjviz.py) is to provide basic visualization using rdf log file. There is no required dependency other pyjanitor modules required.
pyjviz.py uses two modules: [rdflib](https://rdflib.readthedocs.io/en/stable/) and [graphviz](https://github.com/xflr6/graphviz) to implement pipe execution trace graph. rdflib provides [[SPARQL]] implementation which used to query rdflIb. The SPARQL queries results then formatted to graphviz [[dot]] in-memory file and using python graphviz function dumped to resulting .png file.

