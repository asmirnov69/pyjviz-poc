# pyjviz-poc

this repo is built to describe the idea to have some new features added in pyjanitor:
- to help users have diagrams of their method chains runtime behavior. it is done via introduction of mechanism to collect the data during pyjanitor chained method calls. The data collected are to be stored as RDF/tutle file. Later it is possible to use provided visualisation scripts to present collected trace as diagram - looks here as example how it looks like ...

- to introduce CMP (Chained Methods Pipe). CMP is the class to enable users so they can provide additional information to chained method contruct used extensevly by pyjanitor. Proposed above pyjanitor visualization will put CMP to immediate use - see examples in scripts/dirty-clean-w-cmp.py and notebooks/conditional-join-w-cmp.ipynb

Besides feature proposals the repo code is trying illustrate the idea of using RDF as format to collect log files and possibly some other pyjanitor-related data (types parsed using separate ast-based tools).

With immediate focus to visualization using rdflib-SPARQL and graphviz we can start the discussion (and possibly planning) around bigger idea of rdf logs and similarily collected data to be stored in graph database. This would be database of research&production activity which uses SPARQL and/or opencypher to provide the way to connect collected data to other knowledge graph systems (e.g. Obsidian). Such database and its integrations is expected to help with research experiments and production tasks in a new way where it will be possible to search through past work results using one's favorite knowledge-base exploration system (and maybe build new ones).

## How to run examples

Examples are in notebooks/ and scripts/. You can run it without pyjanitor. I am running evrything using venv and pip installs. Both scripts and notebooks refers to code in pyjviz-poc/janitor via dircet usage of sys.path. So if you want to run scripts your current working directory should be pyjviz-poc/scripts.

scrips and nodebooks will create or overwrite file rdflog.ttl. This is the trace of chained mathod executions. To see diagram of the trace call show-rdflog.py - it will produce rdflog.ttl.png which you can view in any suitable png viewer (browser, jupyter etc)

## repo directories

- data/ -- some data to be used by examples in scripts/ and notebooks/
- janitor/ -- this is mostly code form pyjanitor/janitor to make original pyjanitor examples work. The few files are added to create some additional functionality which is the core of the proposal. That additional files are described below in ...
- learn-graphviz/ -- place where some examples stored to help understand how thing work in graphviz
- notebooks/ -- pyjanitor jupyter notebook examples with some additions to make show-rdflog.ipynb notebook work
- scripts/ -- pyjanitor examples in the form of scripts. you will need to be in this directory to run them

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

     def async_run(self) -> None:
     """
     Spawn func call on thread
     """
     self.call_thread = new_thread.call(self.cmp_func)
     return self

     def wait(self) -> DataFrame:
     """
     waits and returns once result available
     """
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
```
