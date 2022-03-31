import argparse
import csv
import os
import sys

from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from src.syllable import SyllableBuilder, Syllable

# TODO: refactor a bit (program by intention)


def convert_lexicon_element(element, use_tones=True):
    word = element[1]
    pronunciations = [element[2]]  # TODO: handle the extra columns when ready

    converted_elements = []
    for pronunciation in pronunciations:
        syllable_phonemes = [syllable.split(" ")
                             for syllable in pronunciation.split(" . ")]
    
        # temp workaround
        for i, elem in enumerate(syllable_phonemes):
            if len(elem) < 2 or len(elem) > 4:
                print(f"Syllable {elem} has {len(elem)} phonemes, dropping from dict")
                syllable_phonemes.pop(i)
                
        syllables = [SyllableBuilder.from_phonemes(phonemes)
                     for phonemes in syllable_phonemes]
        mfa_pronunciation = " ".join(
            [syllable.serialize(use_tones) for syllable in syllables]).replace("_", "")
        converted_elements += [word, mfa_pronunciation]

    return converted_elements


def _tokenize_syllables(syllables):
    return [syllables.split(" ") for syllable in syllables]


def main(args):

    with open(args.lexicon, "r") as tsvin, open(args.outputFile, "w") as tsvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        tsvout = csv.writer(tsvout, delimiter='\t')

        for row in tsvin:
            mfa_elements = convert_lexicon_element(row, args.use_tones)
            tsvout.writerow(mfa_elements)


# Usage
# python process-lexicon.py -i input.txt -o output.txt -t
# (-t optional, see help)
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='converts lexicon to MFA dictionary')
    parser.add_argument('-i',
                        required=True,
                        help='lexicon txt file (assumes tab separation)',
                        type=str,
                        dest='lexicon'
                        )
    parser.add_argument('-o',
                        required=True,
                        help='mfa-ready output file',
                        type=str,
                        dest='outputFile'
                        )
    parser.add_argument('-nt', '--no-tones', dest='use_tones', action='store_false',
                        help='do not include tones in the output (default: included)'
                        )
    parser.add_argument('-t', '--tones', dest='use_tones', action='store_true',
                        help='include tones in the output (default: included)'
                        )
    parser.set_defaults(tones=True)
    args = parser.parse_args()

    main(args)
