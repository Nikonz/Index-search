#!/bin/bash

rm -rf ./files
mkdir files
python ./src/index.py "$@"
