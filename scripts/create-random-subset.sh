#!/bin/bash

### Functions ###

error() { printf "%s\n" "$1" >&2; exit 1; }

num_random_filenames() {
    local data=$1
    local num=$2
    basename --suffix=inLine.wav -- "$data"*inLine.wav | shuf -n "$num"
}

### Script ###

data="$1/"
num=$2
out_dir="./random_subset_${num}/"
mkdir "${out_dir}" || error "Rename existing directory or try another subset size."

mapfile -t samples < <(num_random_filenames "$data" "$num")
for sample in "${samples[@]}"; do 
    cp "${data}${sample}inLine.wav" "${out_dir}${sample}inLine.wav"
    cp "${data}${sample}outLine.wav" "${out_dir}${sample}outLine.wav"
    cp "${data}${sample}inLine.TextGrid" "${out_dir}${sample}inLine.TextGrid"
    cp "${data}${sample}outLine.TextGrid" "${out_dir}${sample}outLine.TextGrid"
done
echo "copied ${num} file sets (inLine, outLine, .wav, .TextGrid) from ${data} to ./output/"
