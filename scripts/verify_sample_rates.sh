#!/bin/sh

# Input: ($1) the directory containing the .wav files to verify 
# Output: to STDOUT,  the sample rates for each .wav file
audio_dir=$1
find "$audio_dir" -type f -name "*.wav" -exec sox --info {} \; | grep "Sample Rate"
