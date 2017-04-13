# ESIPDroneClusterData

Currently this project contains some initial data processing scripts and some sample Drone 
CO2Meter profile logs (manifested as [CSV](https://en.wikipedia.org/wiki/Comma-separated_values)).

# Requirements

 * [Python](https://www.python.org/) tested with 3.5.1

# Usage 
Use the [src/main.py](https://github.com/ESIPFed/ESIPDroneClusterSoftware/blob/master/src/main.py) 
script to make plots, see 
[example/README](https://github.com/ESIPFed/ESIPDroneClusterSoftware/blob/master/example/README.md) 
for a HOWTO and or run 
```
$ python src/main.py -h
```

# Serializing the Sample CSV Data as RDF

It has become a topic of interest to experiment with mapping Drone data into 
[linked data](https://www.w3.org/standards/semanticweb/data)
manifestations in order to provide an environment where applications can query 
the data, draw inferences using vocabularies, etc.

[Apache Any23](http://any23.apache.org) is a Java library, a web service and a 
command line tool that extracts structured data in RDF format from a variety of Web documents.
Users can easily use the [Any23 CSV Extraction Algorithm](http://any23.apache.org/dev-csv-extractor.html)
to serialize the CSV data as one of a number of Semantic Web formats such as json, nquads, ntriples, 
rdfxml, trix, turtle and uri's. The guide below displays exactly how you can do this,

## Requirements
 * Java 8
 * [Apache Maven](http://maven.apache.org)

First download the Any23 source and install it
```
$ cd /usr/local
$ git clone https://github.com/apache/any23.git && cd any23
$ mvn install -DskipTests
```
The run the [Any23 Command Line Interface](http://any23.apache.org/getting-started.html#Use_the_Apache_Any23_CLI) 
tooling. The following assumes that you have the ESIPDroneClusterSoftware directory located at 
/usr/local/ESIPDroneClusterSoftware

```
$ ./cli/target/appassembler/bin/any23 rover -s -l any23.log -o morning1.ttl -f turtle /usr/local/ESIPDroneClusterSoftware/example/morning1.csv
```
The above commands are explained as follows
```
    rover      Any23 Command Line Tool.
      Usage: rover [options] input IRIs {<url>|<file>}+
        Options:
          -d, --defaultns
             Override the default namespace used to produce statements.
          -e, --extractors
             a comma-separated list of extractors, e.g. rdf-xml,rdf-turtle
             Default: []
          -f, --format
             the output format
             Default: json
          -l, --log
             Produce log within a file.
          -n, --nesting
             Disable production of nesting triples.
             Default: false
          -t, --notrivial
             Filter trivial statements (e.g. CSS related ones).
             Default: false
          -o, --output
             Specify Output file (defaults to standard output)
             Default: java.io.PrintStream@5204062d
          -p, --pedantic
             Validate and fixes HTML content detecting commons issues.
             Default: false
          -s, --stats
             Print out extraction statistics.
             Default: false
```
If you take a look in morning1.ttl, you will now see a Turtle manifestation of the 
[morning1.csv](https://github.com/ESIPFed/ESIPDroneClusterSoftware/blob/master/example/morning1.csv) 
file.

# Querying the Turtle Drone Data

Say we are interested in querying the above drone data we've serialized as Turtle. One way this can be 
achieved is to use the [ESIP Community Ontology Repository](http://cor.esipfed.org/ont/~lmcgibbn/morning1v2)
which hosts the Turtle data.

Using the [SPARQL Search](http://cor.esipfed.org/ont/sparql) functionality, we can submit the following query
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX morning1: <file:/usr/local/ESIPDroneClusterSoftware/example/morning1.csv>

SELECT * WHERE {
  ?sub morning1:Co2Ppm ?value .
  FILTER (?value > 500) .
}
LIMIT 10
```
The simple sample query below gives us the first ten results from the dataset which have CO2 
Concentrations (parts-per-million) of greater than 500 ppm.
