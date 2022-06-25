# MFA installation/alignment workbook notes

## General
- This repository contains a set of scripts and data types to prepare pronunciation dictionaries and audio/transcript files for alignment using the [Montreal Forced Aligner (MFA)](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/formats/corpus_structure.html).

## Installation

### Dependencies

Ensure all of the following programs are discoverable on your terminal PATH. Installation instructions linked where neceesary:

- python 3
- bash (tested on version > 5.0)
- [sph2pipe](https://github.com/burrmill/sph2pipe)
- [praat](https://www.fon.hum.uva.nl/praat/)

### Instructions

- Clone this directory: `git clone https://github.com/michaelhaaf/mfa-workbook.git`
- Run `pip install -r requirements.txt` in your preferred python environment
- Ensure your preferred python environment is version 3.9 or greater
- Run `python -m unittest` to see sample use cases for each script/source file.

## Usage

This guide assumes you are starting with a corpus in the IARPA format:

```
corpus/
|-- scripted/
|   |-- reference_materials/
|   |   |   `-- lexicon.txt
|   |   |   `-- lexicon.sub-train.txt
|   |-- training/
|   |   |-- audio/
|   |   |   `-- recording1.sph
|   |   |   `-- recording2.sph
|   |   |   `-- ...
|   |   |-- transcript_roman/
|   |   |   `-- recording1.txt
|   |   |   `-- recording2.txt
|   |   |   `-- ...
```

To use MFA to align the transcripts with the recordings, however, you need the following [corpus structure](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/formats/corpus_structure.html):

```
`--pronunciation_dictionary.txt
`--textgrid_corpus/
|   `-- recording1.wav
|   `-- recording1.TextGrid
|   `-- recording2.wav
|   `-- recording2.TextGrid
|   `-- ...
```

That is, the following steps need to be taken:

- [Convert bulk generic audio files to 16kHz .wav files](#bulk-audio-conversion)
- [Convert bulk .txt transcripts to .TextGrids](#bulk-transcript-conversion)
- [Convert Iarpa corpus lexicon to MFA-ready pronunciation dictionary](#iarpa-lexicon-to-mfa-dictionary)
- [Prepare all of the above for alignment with MFA](#preparation)

Instructions for each step, using the code in this repository, are given below. You can follow the steps with the data contained in the sample-data directory to get a sense of the process. Sample results for this dataset are also given in the sample-data directory.

## Bulk audio conversion

Iarpa corpus audio files are stored as `.sph` files with an 8kHz sample rate. These files need to be converted to `.wav` and resampled to 16kHz to be recognizable to MFA. 

There exist many tools to convert and resample audio formats, but none that can specifically (1) convert .sph to .wav (2) resample .wav to 16kHz without corrupting the pitch/speed of the audio file (3) handle gigabytes of audio files in bulk without running into RAM issues.

The `bulk_sph_resample` script performs all three functions using (1) [sph2pipe](https://github.com/burrmill/sph2pipe) for conversion (2) [praat](https://www.fon.hum.uva.nl/praat/) for resampling and (3) bash to manage praat scripts as independent shell processes. This allows praat to run resampling on each file individually, preventing all files in the directory from loading into memory at the same time.

The script interactive. Open a terminal in this repository and run:
```shell_session
$ bash ./scripts/bulk_sph_resample ./corpus/scripted/training/audio/
```
`./corpus/scripted/training/audio/` should be replaced by the path to the directory where your .sph audio files are stored. Once run, the script will begin an interactive session. The process should look something as follows:
```shell_session
Checking if there are .sph files in sample-data/iarpa_corpus/scripted/training/audio/...
Found 10 .sph files (note: >1000, some steps may take several minutes)
Convert .sph files to .wav? (y/n)
y
Enter the path of the directory where the new .wav files will be stored:
textgrid_corpus
mkdir: created directory 'textgrid_corpus'
Copying files...
Converting to .wav...
Cleaning up .sph copies...
Resampling...
Resampling complete, see results in textgrid_corpus
```
Note that this script could take anywhere from several minutes to a few hours (the resampling portion especially) depending on the number of audio files you are processing. Once it is complete, the generated .wav audio files are ready for MFA.

You can verify that the conversion/resampling was successful by checking the new .wav files using `sox --info`:
```shell_session
$ find sample-data/textgrid_corpus/ -name "*.wav" -exec sox --info {} \; | grep -e "Input File" -e "Sample Rate"

Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_38698_20111025_181550_C6_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_90313_20111019_153045_O3_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_84543_20111124_194834_SC_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_94149_20111027_122829_L1_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_74395_20111117_132438_T2_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_31441_20111026_001007_C5_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_34961_20111027_173059_S5_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_79495_20111017_194334_O2_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_92735_20111024_165237_SB_scripted.wav'
Sample Rate    : 16000
Input File     : 'sample-data/textgrid_corpus/BABEL_BP_101_31393_20111018_151856_M1_scripted.wav'
Sample Rate    : 16000
```

Your audio files are now ready for MFA.

## Bulk transcript conversion
Iarpa transcript files are stored as `.txt`. These files need to be converted to `.TextGrid`.

The python library `praatio` has useful utilities for performing this conversion. The `txt-to-textgrid.py` script makes use of these utilities to convert a specified directory of `.txt` files to the `.TextGrid` format. The script also converts Iarpa tags (e.g. '\<breath\>') to their MFA equivalent (e.g. '{LG}') along with other syntax related substitutions.

To use `txt-to-textgrid.py`, open a terminal in this repository and run:

```shell_session
$ python3 scripts/txt-to-textgrid.py --input corpus/scripted/training/transcript_roman/ --dest textgrid_corpus/

Processing BABEL_BP_101_38698_20111025_181550_C6_scripted.txt...
Processing BABEL_BP_101_84543_20111124_194834_SC_scripted.txt...
Processing BABEL_BP_101_94149_20111027_122829_L1_scripted.txt...
Processing BABEL_BP_101_34961_20111027_173059_S5_scripted.txt...
Processing BABEL_BP_101_31441_20111026_001007_C5_scripted.txt...
Processing BABEL_BP_101_74395_20111117_132438_T2_scripted.txt...
Processing BABEL_BP_101_79495_20111017_194334_O2_scripted.txt...
Processing BABEL_BP_101_92735_20111024_165237_SB_scripted.txt...
Processing BABEL_BP_101_31393_20111018_151856_M1_scripted.txt...
Processing BABEL_BP_101_90313_20111019_153045_O3_scripted.txt...
BABEL_BP_101_94149_20111027_122829_L1_scripted.TextGrid
BABEL_BP_101_84543_20111124_194834_SC_scripted.TextGrid
BABEL_BP_101_79495_20111017_194334_O2_scripted.TextGrid
BABEL_BP_101_31393_20111018_151856_M1_scripted.TextGrid
BABEL_BP_101_92735_20111024_165237_SB_scripted.TextGrid
BABEL_BP_101_74395_20111117_132438_T2_scripted.TextGrid
BABEL_BP_101_34961_20111027_173059_S5_scripted.TextGrid
BABEL_BP_101_31441_20111026_001007_C5_scripted.TextGrid
BABEL_BP_101_90313_20111019_153045_O3_scripted.TextGrid
BABEL_BP_101_38698_20111025_181550_C6_scripted.TextGrid
```

The `--input` and `--dest` arguments should be replaced by the path to the directory where your .txt transcript files are stored and your desired output directory respectively. Once run, the script will complete automatically. The process should something like shown above.

Confirm that your textgrids look correct using a text editor.

## Iarpa lexicon to MFA dictionary

The Iarpa lexicon format needs to be converted to an MFA pronunciation dictionary.

```shell_session
python scripts/syllabify.py -i sample-data/iarpa_canto_corpus/scripted/reference_materials/lexicon.txt -o ./sample-data/pd-test.txt
```

Confirm that your pronunciation dictionary look correct using a text editor (`vimdiff ./sample-data/pd.txt ./sample-data/pd-test.txt`, for example).

## Preparation

If you followed the steps shown above, you should have a resulting textgrid_corpus directory with prepared audio, transcript, and pronunciation dictionary files ready to be used by MFA. You can validate the results using MFA as follows:

```shell_session
$ conda activate aligner
(aligner) $ mfa validate ./textgrid_corpus/ ./pd.txt
```

MFA should run some diagnostics successfully if the previous steps worked. You can continue with the rest of the training/aligning tutorial [here](https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/index.html#first-steps-align-train-acoustic-model).

Note well: the sample-data/ given in this repository (10 randomly chosen ~10second speech files) is no where near enough data to train a performant model. With this data we are simply verifying that there are no syntax/format issues with your workflow. Once that is verified, you will need to acquire more data to train a performant model. See [this blog post](https://memcauliffe.com/how-much-data-do-you-need-for-a-good-mfa-alignment.html#summing-up) for rough guidelines as to the magnitude of data required to train a model for alignment/general usage.
