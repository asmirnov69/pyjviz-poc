# pyjviz-poc

this repo is built to describe some new features proposed for [pyjanitor](https://github.com/pyjanitor-devs/pyjanitor):

- be able to generate the diagrams of method chains runtime behavior. it is done via introduction of mechanism to collect the data during pyjanitor chained method calls. The data collected are to be stored as RDF/turtle file. Later it is possible to use provided visualisation scripts to present collected trace as diagram - [code example](https://github.com/asmirnov69/pyjviz-poc/blob/main/scripts/dirty-clean.py) --> [diagram](https://github.com/asmirnov69/pyjviz-poc/blob/main/scripts/rdflog/dirty-clean.ttl.dot.png)

- to introduce CMP (Chained Methods Pipe). CMP is the class with purpose to provide additional information to pyjanitor chained method calls. Proposed above pyjanitor visualization will put CMP to immediate use - [code example](https://github.com/asmirnov69/pyjviz-poc/blob/main/scripts/conditional_join_w_cmp.py) --> [diagram](https://github.com/asmirnov69/pyjviz-poc/blob/main/scripts/rdflog/conditional_join_w_cmp.ttl.dot.png)

The implementaion uses pyjanitor code copied intact to pyjviz-poc/janitor directory so few chosen pyjanitor examples will be working.
[register.py from pandas_flavor](https://github.com/Zsailer/pandas_flavor/blob/master/pandas_flavor/register.py) was also copied and modified to have required rdf logging functionality.
<b>pyjviz-poc/janitor/pyj*.py</b> and <b>pyjviz-poc/janitor/functions/pandas_builtin_overrides.py</b> are new files with proposed functionality implementation.

Immediate focus is to have png diagram files generation working using rdflib with provided SPARQL and graphviz. There is a bigger idea of rdf logs and similarily collected data to be stored in graph database. This would be database of research&production activity which uses SPARQL and/or opencypher to provide the way to connect collected data to other knowledge graph systems (e.g. Obsidian).

## How to run examples

For venv users it is possible to use this sequence:

```
python3 -m venv ~/venv/pyjviz
source ~/venv/pyjviz/bin/active

cd pyjviz-poc
pip install -r requirements.txt
```

After that one can run scripts from pyjviz-poc/scripts directory

```
cd scripts # pwd should show 'pyjviz-poc/scripts'

python a0.py
python dirty-clean.py
python dirty-clean-w-cmp.py
python conditional_join.py
python conditional_join_w_cmp.py
```

Results will be on the screen and in directory pyjviz-poc/scripts/rdflog

You should be able to run notebooks in pyjviz-poc/notebooks using packages listed in pyjviz-poc/requirements.txt
Diagram will be shown at the last cell output.

Install commands for jupyterlab which were working for me (after pip install -r requirements.txt):

```
cd pyjviz-poc
pip install jupyterlab
jupyter lab
```

