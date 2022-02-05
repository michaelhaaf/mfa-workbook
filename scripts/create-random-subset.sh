#!/bin/bash
set -e
set -u

### Functions ###

error() { printf "%s\n" "$1" >&2; exit 1; }

num_random_filenames() {
    local data=$1
    local num=$2
    basename --suffix=.wav -- "$data"*.wav | shuf -n "$num"
}

### Script ###

data="$1/"
num=$2
out_dir="./random_subset_${num}/"
mkdir "${out_dir}" || error "Rename existing directory or try another subset size."

mapfile -t samples < <(num_random_filenames "$data" "$num")
for sample in "${samples[@]}"; do 
    cp "${data}${sample}.wav" "${out_dir}${sample}.wav"
    cp "${data}${sample}.TextGrid" "${out_dir}${sample}.TextGrid"
done
echo "copied ${num} file sets (.wav, .TextGrid) from ${data} to ${out_dir}"
