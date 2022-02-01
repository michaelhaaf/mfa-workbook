#!/bin/bash

# Input: ($1) the directory containing the .wav files to verify 
# Output: for each file in $1
#   - if sample rate is 16KHz, indicate that no changes need to be made
#   - otherwise, attempt resample

# audio_dir=$1
# find "$audio_dir" -maxdepth 1 -type f -name "*.wav" -exec sox --info {} \; |
#     awk '/Input File/ {printf $4"\t"} /Sample Rate/ {print $4"\t"}' |
#     xargs -n1 [[ $(awk '{print $2}') == "16000" ]] && echo "yes" || echo "no"

# TODO: divide in two stages, one where we just count to see if any are not 16kHz; print success if they all are
#       otherwise, prompt to ask if generating upsamples is what you want to do.

audio_dir=$1
output_dir=$2
for f in "$audio_dir"*.wav; do
    sample_rate="$(sox --info "$f" | awk '/Sample Rate/ {print $4}')";
    echo "$f: sample rate $sample_rate Hz";
    if [[ $sample_rate != "26000" ]] ; then 
        mkdir -p "$output_dir";
        echo "... resampling to 16kHz";
        sox -r 16000 "$f" "$output_dir${f##*/}"
    fi
done
