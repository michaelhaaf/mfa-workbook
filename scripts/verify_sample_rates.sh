#!/bin/bash

### Script Usage and Parameters ###

help_message()
{
    echo "Usage: verify_sample_rates [-h] DIRECTORY"
    echo "Checks .wav files located in DIRECTORY."
    echo 
    echo "Helper script to automatically scan the sample rates of a directory of .wav files."
    echo "If the sample rate is not 16kHz, prompt the user to generate new .wavs with 16kHz sample rate"
    echo
    echo "options:"
    echo "-h     Print this help message."
    echo
}

while getopts ":h" o; do case "${o}" in
	h) help_message && exit ;;
	\?) printf "Invalid option: -%s\\n" "$OPTARG" && exit 1 ;;
esac done

shift $((OPTIND - 1));  

[[ -z $1 ]] && help_message && exit 1;
audio_dir=$1 

### Functions ###

error() { printf "%s\n" "$1" >&2; exit 1; }

check_sample_rates() { \
    echo "Checking (may take a minute if >10k files)..."
    echo "[Number of files] [sample rate in Hz]:"
    find "$audio_dir" -maxdepth 1 -type f -name "*.wav" -exec sox --info {} \; |
        awk '/Sample Rate/ {print $4}' | sort | uniq -c 
}

confirm_before_resample() { \
    echo "Create new directory with .wav files resampled at 16kHz? (y/n)"
    read -r input
    [[ ! $input = "y" ]] && return 1
    return 0
}

prompt_output_directory() { \
    echo "Enter the path of the directory where the new .wav files will be stored:"
    read -r -e -p "" output_dir
    mkdir -p -v "$output_dir"
}

generate_resamples() { \
    for f in "$audio_dir"*.wav; do
        local output_path="$output_dir/${f##*/}"
        sox -r 16000 "$f" "$output_path" 
        echo "Created new 16kHz .wav file at $output_path."
    done
}

### Script ###
check_sample_rates 
confirm_before_resample || error "No resampling will be performed. Exiting."
prompt_output_directory
generate_resamples 
exit 0
