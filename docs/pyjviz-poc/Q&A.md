selected questions with some answers

# Questions from issue #1176 discussion

issue #1176 -> https://github.com/pyjanitor-devs/pyjanitor/issues/1176#issuecomment-1313514296

## What is the purpose of ChainedMethodsCall introduction?
Main idea of [[ChainedMethodsCall]] introduction is to provide the way to describe chained methods as a group of visual primitives. It seems to be appropriate in some situations where transformations become big enough.

There is also still unclear idea to use [[ChainedMethodsCall]] for static analysis utility. Using [[ast]] or similar parser it seems to be possible to retrieve useful information about [[pyjanitor]] transforms before run-time. Such information could be saved to [[RDF]]] dataset to provide static visualization with additional things like context help using code annotations, docstrings or similar content.

## What are the most likely ways this code would break in the future, and what's the most likely place to go and fix?
[README](README.md) code is written using global objects in few places in [pandas_flavor](pandas_flavor.md) and [[Implementation plan#^041966|pyjrdflogger.py]]. Proposal implementation should be fine for single-threaded use. However it would be good idea to have real implementation to address possible use of [[pyjanitor]] transformations from multiple threads. I don't see any other obvious places where proposed implementation can break.

## What are desired possible future improvements not covered in this PR, and where should the code changes be made?
Possible future directions are described in [[README#^d40b47|Further development]]. It include static visualization idea described in Q1 [[tbc]] `how to refer to Q1 using link features provided by obsidian`

As for code change locations the decisions need to be made about how [[pyjanitor]] distribution will look like.
Once changes to implement [[RDFLogger]] and [[ChainedMethodsCall]] are done in core [[pyjanitor]] and [[pandas_flavor]] the rest of visualization and other utilities can be implemented as additional python and/or js modules and utilities in corresponding code repo. It is possible to do in robust manner using [[RDF#^ac6f28|SHACL]] validator to synchronize [[RDFLogger]] output schema  changes.

It is also possible to keep some basic features in [[pyjanitor]] itself to have something working out-of-the-box for [[Jupyter]] users
