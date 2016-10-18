# Index & Search

This repository contains a part of an implementation of a simple search engine. 
If you have already downloaded all pages you need, you can use it to build index and make search over it.

# Prerequisites

You need Python 2.7 and Bash to use this engine correctly.

# How to use

## Index

First of all, you need to build an index. To do it you should run the following command:

`./index.sh encType sample/1.gz sample/2.gz sample/3.gz ...`

where `encType` should be "simple9" or "varbyte" (depends on how you want to encode index). 
And after encType you should print paths to all the documents, each of which should contain the information about some internet pages in format decribed below:

#### Format of the documents

## Making of a dictionary

Then, you need to build a dictionary for quick search. You can do it by running the following command:

`./make_dict.sh`

## Search

Finally, after completing two previous steps, you can use the main part. Congrats! :) To start searching, run:

`./search.sh`

Each line you print will be a single query. To stop searching just use SIGTERM.

#### Input format

In your queries you can any words and also special symbols: `(`, `)`, `&`. `|`, `!`. So you can make quite complicated queries, if you want.

#### Output format

For each query engine will print number of matching urls at the first line. And then there will be printed all these urls, divided with a `\n` symbol.
Each url can be printed only one time for a single query.
