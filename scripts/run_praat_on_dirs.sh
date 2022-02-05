#!/usr/bin/env bash
set -e 
set -u

mapfile -t dirs < <(find . -maxdepth 1 -type d -name "[0-9][0-9]" -printf "%p\n")

for dir in "${dirs[@]}"; do
    echo "$dir" |
    awk '{
        printf "cd %s;", $0
        printf "echo Running resamples on .wavs in %s...;", $0
        printf "praat --run ./connie.praat;"
        printf "cd ../;"
        printf "sleep 10;"
    }' | bash
done

