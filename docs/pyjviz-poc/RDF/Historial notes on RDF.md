# Historical perspective
It used to be XML. XML heavy promotion produced some results but overall didn't meet the expectations.
RDF is exactly opposite story: quite possible it is one the most underrated SE innovation. The text below is an attempt to introduce RDF as tool for software engineers. Some of them may have tried to understand RDF and related tools. Because of some unclear reasons the research activity become completely concentrated on using of RDF as knowledge representation approach and related matters like ontologies, boolean algebra application to provide expressive power etc. If you would try to explore you stumble to simple questions like 'how do I use OWL ontology' or 'what is entailment regime and why should I care'

As outcome of early RDF standartization efftort SPARQL emerged as query language for RDF datasets. It is powerful query tool for general researchers in non-quantative fields. But deficiency of whole approach make life of those researchers very complicated - there was no way to impose structure on RDF dataset in the way how relational database do. It was nothing which looked like 'schema'. That was major block for SE usage of RDF and related tools.

SHACL arrival have changed this picture. It became possible to define 'schema' in precise and useful way for RDF datasets.

Meanwhile power of the idea to use graph as foundation of database technology was utilized with significant success by Neo4J. Neo4J uses different approach for data representation - LPG. If you start looking more closely you could arrive to impression that it is actually the same thing as RDF triple-based representation.
