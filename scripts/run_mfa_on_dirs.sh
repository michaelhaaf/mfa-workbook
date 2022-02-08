#!/usr/bin/env bash
set -e 
set -u

data_dir=$1
dict=$2
output_dir=$3

mapfile -t dirs < <(find "$data_dir" -maxdepth 1 -type d -name "[0-9][0-9]" -printf "%p\n")

for dir in "${dirs[@]}"; do
    echo "$dir" | awk -v dir="$dir" -v dict="$dict" output="$output_dir$(basename "$dir")" \
    '{
        printf "echo Running mfa train on dir %s...;", dir
        printf "mfa train %s %s %s;", dir, dict, output
        printf "sleep 2;"
    }' | bash
done

