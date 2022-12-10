main doc - https://www.w3.org/TR/shacl/

Q: closed class hierarchy - *dash:closedByTypes*
	answer with solution - https://stackoverflow.com/a/70808935/1181482
	exact example of *dash:closedByTypes* usage https://datashapes.org/constraints.html#ClosedByTypesConstraintComponent
	looks like for *dash:closedByTypes* to work the classes and subclasses must be described in both data and schema for properly working [[#TopQuadrant (validator)]]
	example in `pyjviz-poc/rdf-examples/minimal-shacl-example`

# TopQuadrant (validator)

- https://github.com/TopQuadrant/shacl - SHACL validator implementation by original author - Holger Knublauch ([holger@topquadrant.com](mailto:holger@topquadrant.com))
- binary distributions: https://repo1.maven.org/maven2/org/topbraid/shacl/

I am using shacl-1.4.2 with default-jre on ubuntu 22
```
openjdk version "11.0.17" 2022-10-18
OpenJDK Runtime Environment (build 11.0.17+8-post-Ubuntu-1ubuntu222.04)
OpenJDK 64-Bit Server VM (build 11.0.17+8-post-Ubuntu-1ubuntu222.04, mixed mode, sharing)
```

cmd example:
```
sh ~/shacl-1.4.2/bin/shaclvalidate.sh -datafile test.ttl -shapesfile test.shacl.ttl
```
