#!/usr/bin/env bash
set -e 
set -u

cmd_find=(find . -maxdepth 1 -type f -name "*.wav" -printf "%p\n")

"${cmd_find[@]}" | awk '{d=substr($0,16,2) ; printf "mkdir -p %s ; mv %s %s\n",d,$1,d }' | bash
