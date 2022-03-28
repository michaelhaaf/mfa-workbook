#!/usr/bin/env bash
set -e 
set -u
set -x

data_dir=$1
dict=$2
output_dir=$3

mapfile -t dirs < <(find "$data_dir" -maxdepth 1 -type d -name "[0-9][0-9]" -printf "%p\n")

for dir in "${dirs[@]}"; do
    echo "$dir" | awk -v sub_dir="$dir" -v dict="$dict" -v output="$output_dir/$(basename "$dir")" \
    '{
        printf "echo Running mfa train on dir %s...;", sub_dir
        printf "mfa train %s %s %s;", sub_dir, dict, output
        printf "sleep 2;"
    }' | bash
done

