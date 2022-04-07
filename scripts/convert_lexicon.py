#!/usr/bin/env python3

import argparse
import csv
import os
import sys
import yaml
import dacite

from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from src.lexicon import Lexicon, LexiconIO, Configuration

def main(args):

    # TODO: move to actual yaml files, load programmatically from user input
    input_cfg = yaml.safe_load(
        """
    lexicon: IARPA_CANTO
    pronunciation_bound: "\t"
    syllable_bound: " . "
    phoneme_bound: " "
    tokens_to_remove: ""
    include_tones: true
    """
    )

    output_cfg = yaml.safe_load(
        """
    lexicon: MFA
    pronunciation_bound: "\t"
    syllable_bound: " "
    phoneme_bound: ""
    tokens_to_remove: "_"
    include_tones: true
    """
    )

    converters = {Lexicon: lambda x: Lexicon[x]}

    output_config = dacite.from_dict(
        data_class=Configuration,
        data=output_cfg,
        config=dacite.Config(type_hooks=converters)
    )

    input_config = dacite.from_dict(
        data_class=Configuration,
        data=input_cfg,
        config=dacite.Config(type_hooks=converters)
    )

    lexiconIO = LexiconIO(input_config=input_config,
                          output_config=output_config)

    with open(args.lexicon, "r") as tsvin, open(args.outputFile, "w") as tsvout:
        tsvin = csv.reader(tsvin, delimiter=input_config.pronunciation_bound)
        tsvout = csv.writer(tsvout, delimiter=output_config.pronunciation_bound)

        for entry in tsvin:
            (word, pronunciations) = lexiconIO.deserialize(entry)
            output_entries = [lexiconIO.serialize(word, p) for p in pronunciations]
            for p in output_entries:
                tsvout.writerow(p)


# Usage
# python process-lexicon.py -i input.txt -o output.txt -f INPUT_LEXICON_FORMAT
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='uses Lexicon and Syllable libraries to convert lexicon of specified format and language to MFA pronunciation dictionary')
    parser.add_argument('-i',
                        required=True,
                        help='lexicon txt file',
                        type=str,
                        dest='lexicon'
                        )
    parser.add_argument('-o',
                        required=True,
                        help='mfa-ready output destination',
                        type=str,
                        dest='outputFile'
                        )
    parser.add_argument('-f',
                        dest='format',
                        help='input lexicon format',
                        choices=Lexicon.__members__
                        )
    args = parser.parse_args()

    main(args)
