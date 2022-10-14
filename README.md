# pyjviz-poc

this repo is built to describe the idea to have pyjanitor feature(s) to be developer to help users:
- to have visual representation of their method chaines (and additional features like pipes introduced in *_w_pipes.py and *_w_pipes.ipynb examples
- to illustrate the idea of doing so using rdf-based log file with subsequent visualization using rdflib (w SPARQL) and graphviz
- to start some discussions (and possibly planning) around bigger idea of having rdf logs stored into graph database of research runs.
  such database suppose to help with research experiments and production is a new way where it will be possible to search through past work results
  using one's favorite knowledge-base exploration system and maybe build new ones. Currently efforts in this direction are all around
  SPARQL as readily available via rdflib package.

## repo directories

- data -- some data to be used by examples in scripts/ and notebooks/
- janitor -- this is mostly code form pyjanitor/janitor to make original pyjanitor examples work. The few files are added to create some additional functionality which is the core of the proposal. That additional files are described below in ...
- learn-graphviz -- place where some examples stored to help understand how thing work in graphviz
- notebooks - pyjanitor jupyter notebook examples with some additions to make show-rdflog.ipynb notebook work
- scripts - pyjanitor examples in the form of scripts. you will need to be in this directory to run them
