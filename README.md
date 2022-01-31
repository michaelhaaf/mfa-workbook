# MFA installation/alignment workbook notes

## General
- This repository contains a set of scripts and data types to prepare pronunciation dictionaries and audio/transcript files for alignment using the Montreal Forced Aligner (link).

## Capabilities
- Convert .txt transcripts to .TextGrids
- Convert Iarpa corpus lexicon to MFA-ready lexicon

## Future work
- General serializer/deserializer pattern to adapt to any public corpus for MFA lexicon prep
- Incorporate into polyglotDB (link)

## Installation
- pip install -r requirements.txt
- python -m unittest

## Usage

### .txt to .TextGrid
- From the root directory of the repository:
- python scripts/txt-to-textgrid.py --input <path to folder containing .txts> --dest <path where output .TextGrids will be placed>

### Iarpa lexicon to MFA lexicon
