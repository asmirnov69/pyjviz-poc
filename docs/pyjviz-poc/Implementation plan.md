# Implementation plan of pyjviz-poc proposal

The steps to implement [pyjviz-poc](pyjviz-poc.md) proposal as set of new [pyjanitor](pyjanitor.md) features are outlined below.

## modifications in pandas_flavor module
required modifications in [pandas_flavor](pandas_flavor.md) has to be done to place method call interception logic with optional passing of collected method call name and args to [[RDFLogger]] methods. [pyjviz-poc](pyjviz-poc.md) provides its own version of register.py to implement required logic for the case of pandas dataframe - https://github.com/asmirnov69/pyjviz-poc/blob/ab322f5342f9471bfb9d748bf551bb7f3d5a333e/janitor/register.py#L48
All other cases supported by [pyjanitor](pyjanitor.md) would require similar modifications.

## modifications in pyjanitor
### add functions/pandas_builtin_overrides.py
[pyjviz-poc](pyjviz-poc.md) version of *functions/pandas_builtin_overrides.py* has code to substitute [[pandas]] methods with versions registered to handle method call intercept using [pyjanitor](pyjanitor.md) standard approach using register wrapper.
NOTE that similar implementation is required for all other packages supported by [pyjanitor](pyjanitor.md) -- spark, xarrays [[tbc]]`provide full and verified list`

### add pyjrdflogger.py
the way how enable/disable rdf logger should be designed.  If there is any plan to introduce [pyjanitor](pyjanitor.md) config file it could be statement in there. POC way of doing rdf logger initialization may also be supported as hard-coded override of configuration.

### add pyjviz.py
*pyjviz.py* implementation uses [[rdflib]] and [graphviz](graphviz.md) modules. Those are new dependencies for *pyjanitor*. It could be good opportunity to introduce tunable installation to avoid adding [rdflib](rdflib.md) and [graphviz](graphviz.md) as *pyjanitor* core dependencies

# Further development

^d40b47

## introduce SHACL schema for RDFLogger output
SHACL schema provide the way to describe the [RDFLogger](RDFLogger.md) output using SHACL definitions. It will provide the way to start using rdf logs as parts of bigger knowledge bases.

## user-defined additions to RDFLogger output
[[tbc]]users of *pyjanitor* would possibly find useful ways of feature where they can insert additional rdf triples into rdf logs produced by their code. applications are numerous - visualizations, data catalogs, support for data exploration, ETL support.

## build pyjanitor code static analysis and visualizer
It seems to be possible task to write python code for static analysis and visualization of [ChainedMethodsCall](ChainedMethodsCall.md) usage in user's and other related to *pyjanitor* code which will be based [python3 annotations](python3%20annotations) and code docstrings. The tool will generate rdf dataset which could be compatible with [RDFLogger](RDFLogger.md) output. Main purpose of doing that would be to allow visualizations of *pyjanitor* code before run-time.

## build GUI browser for exploration of RDFLogger and similarly produced  RDF datasets
This is very big task in graph database visualization space. It could be started as separate related project to address some immediate needs of [pyjanitor](pyjanitor.md) users and outline the way how more comprehensive system should look like.
