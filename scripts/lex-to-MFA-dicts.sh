#!/bin/bash

###
# Arguments: 
# 	($1) the lexicon .txt file 
# 	($2) Path to output.txt: MFA pronunciation dictionary (without tones)
# 	($3) Path to output.txt: MFA pronunciation dict (with tones)
# Usage:
#	$ ./lex-to-dicts.sh <lexicon.txt> <output1.txt> <output2.txt>
#
# Sample input/output line:
# 	
#	Input:		V_C_D	wi1si1di1	w i: _1 . s i: _1 . d i: _1
#	MFA dict 1: 		wi1si1di1	w i: s i: d i:
#	MFA dict 2:		wi1si1di1	w i:1 s i:1 d i:1
# 
# Notes and assumptions:
# 	- the token " _[0-6]" indicates tones 0 through 6
# 	- the token " ." is ignored
#	- tone tokens are paired with the token to their left (just remove " _")
#	- token + tone_token = phoneme (nuclei token does not have to be vowel)
#	- original file has entries with >3 columns. Ignored for now, see TODO
###

lexicon=$1
mfa1=$2
mfa2=$3

# TODO: use extra columns (append row for each word -> pronunciation map)
# extra_columns=$(cat "$lexicon" | awk -F "\t" 'NF>3')

sed -E "s/ (_[0-9]|\.)//g" "$lexicon" | cut -f2-3 > "$mfa1"
sed -E "s/ (_|\.)//g" "$lexicon" | cut -f2-3 > "$mfa2"


