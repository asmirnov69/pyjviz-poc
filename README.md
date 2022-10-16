# pyjviz-poc

this repo is built to describe some new features proposed for pyjanitor:

- be able to generate the diagrams of method chains runtime behavior. it is done via introduction of mechanism to collect the data during pyjanitor chained method calls. The data collected are to be stored as RDF/turtle file. Later it is possible to use provided visualisation scripts to present collected trace as diagram - looks here as example how it looks like ...

- to introduce CMP (Chained Methods Pipe). CMP is the class with purpose to provide additional information to pyjanotor chained method calls. Proposed above pyjanitor visualization will put CMP to immediate use - see examples in scripts/dirty-clean-w-cmp.py and notebooks/conditional-join-w-cmp.ipynb

The implementaion uses pyjanitor code copied intact to pyjviz-poc/janitor directory so chosen pyjanitor examples work.
https://github.com/Zsailer/pandas_flavor/blob/master/pandas_flavor/register.py was also copied and modified to have required rdf logging functionality.
pyjviz-poc/janitor/pyj*.py are new files with proposed functionality implementation.

Immediate focus is to have png diagram files generation working using rdflib with provided SPARQL and graphviz. There is a bigger idea of rdf logs and similarily collected data to be stored in graph database. This would be database of research&production activity which uses SPARQL and/or opencypher to provide the way to connect collected data to other knowledge graph systems (e.g. Obsidian).

## How to run examples

To run scripts you need to change current working directoty to scripts and then run it like this:

```
cd scripts
python a0.py
```

It will produce rdf log and png in subdir scripts/rdflog.

Notebooks can be run as usual via jupyter. Diagram will be shown at last cell output.

## repo directories

- data/ -- some data to be used by examples in scripts/ and notebooks/
- janitor/ -- this is mostly code form pyjanitor/janitor to make original pyjanitor examples work. The few files are added to create some additional functionality which is the core of the proposal. That additional files are described below in ...
- notebooks/ -- pyjanitor jupyter notebook examples with some additions to make show-rdflog.ipynb notebook work
- scripts/ -- pyjanitor examples in the form of scripts. you will need to be in this directory to run them

