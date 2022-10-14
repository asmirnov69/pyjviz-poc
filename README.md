# pyjviz-poc

this repo is built to describe the idea to have some new feature(s) in pyjanitor to help users:
- have diagrams of their method chains runtime. CCR (Chained-Call-Return) is terminology invented with purpose to avoid highly overloaded word 'pipe' when we are talking about such language contruct.
CCR is essentially the way how pyjanitor is used - the chains of method calls based on prev link returns. CCRs direct support is introduced in *_w_ccr.py
and *_w_ccr.ipynb examples, see below for more info.
- illustrate the idea of creating of such diagrams using rdf-based log file with subsequent visualization using SPARQL queries hitting collected rdf execution logs
- to start some discussions (and possibly planning) around bigger idea of having functionality added to pyjanitor to enable rdf logging of pyjanitor supported
  types. rdf logs suppose to be stored into graph database of research&production activity. such database is expected to help with research experiments
  and production tasks in a new way where it will be possible to search through past work results using one's favorite knowledge-base exploration system
  (and maybe build new ones). Currently efforts in this direction are all around SPARQL and graphviz as readily available packages. SPARQL implementation
  used is part of rdflib package.

## repo directories

- data/ -- some data to be used by examples in scripts/ and notebooks/
- janitor/ -- this is mostly code form pyjanitor/janitor to make original pyjanitor examples work. The few files are added to create some additional functionality which is the core of the proposal. That additional files are described below in ...
- learn-graphviz/ -- place where some examples stored to help understand how thing work in graphviz
- notebooks/ -- pyjanitor jupyter notebook examples with some additions to make show-rdflog.ipynb notebook work
- scripts/ -- pyjanitor examples in the form of scripts. you will need to be in this directory to run them
