#!/bin/sh

# Input: ($1) the lexicon (assumed 3 column, with tone markers)
# Output: to STDOUT, the result of removing the first column and all tone markers

lexicon=$1
sed "s/_[0-9] \. //g" "$lexicon" | cut -f2-

