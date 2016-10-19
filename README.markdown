# Index & Search

This repository contains partial implementation of a simple search engine. 
If you have already downloaded all pages you need, you can use it to build index and perform search requests.

# Prerequisites

You need Python 2.7, Bash and Google.Protobuf to use this engine properly. All about protobuf you can read [here](https://github.com/google/protobuf).

# How to use

## Index building

First of all, you need to build an index with command:

`./index.sh ENCTYPE FILES...`

where `ENCTYPE` is either "simple9" or "varbyte", depending on index encoding algorithm. 

`FILES` is a list of documents in format, described [here](https://github.com/Nikonz/Index-search#format-of-the-documents).

Example: `./index simple9 sample/{1,2,3}.gz`

#### Format of the documents

Each document can contain a lot of pages. For each of them there should be url and text after it.
All data must be serialized using google.protobuf.
For more information read [this](https://github.com/Nikonz/Index-search/blob/master/src/docreader.py) and [view samples](https://github.com/Nikonz/Index-search/tree/master/samples).

Also, each document can be packed to ".gz" archieve, if needed.

## Dictionary building

After index is created, you need to build a dictionary for quick search with the following command:

`./make_dict.sh`

## Search

Finally, you actually perform search requests. Congrats! :bowtie:. To start searching, run:

`./search.sh`

Each line you print will be a single query. To stop searching just use `SIGTERM`.

#### Input format

You can use any words or special symbols, such as `(`, `)`, `&`. `|`, `!` to make complex queries.

#### Output format

For each query engine will print the number of matching urls at the first line, followed by `LF` separated links that matched the query.
Each url is printed once per single query.
