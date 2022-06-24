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

from src.corpus import Corpus, CorpusFactory
from src.io import FileIO, Request, SyllableRequest
from src.config import Config


# TODO: might not need dacite afterall
def load_configs(input_format, output_format):
    with open(f"config/{input_format}.yaml", "r") as input_config, open(f"config/{output_format}.yaml", "r") as output_config:
        output_config = dacite.from_dict(
                data_class=Configuration,
                data=yaml.safe_load(output_config),
                config=dacite.Config()
                )
        input_config = dacite.from_dict(
                data_class=Configuration,
                data=yaml.safe_load(input_config),
                config=dacite.Config()
                )
        return input_config, output_config



def main(args):

    input_config, output_config = load_configs(args.format.lower(), "mfa")
    input_corpus = CorpusFactory().create(input_config)
    output_corpus = CorpusFactory().create(output_config)
    fileio = FileIO(input_config, output_config)

    requests = fileio.import(args.input_lexicon)
    syllable_requests = [input_corpus.syllabify(r) for r in requests]
    responses = [output_corpus.desyllabify(r) for r in syllable_requests]
    fileio.export(args.output_dict, responses)


# Usage
# python process-lexicon.py -i input.txt -o output.txt -f INPUT_LEXICON_FORMAT
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Convert lexicon of specified format and language to MFA pronunciation dictionary')
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
                        dest='output_dict'
                        )
    parser.add_argument('-f',
                        required=True,
                        dest='format',
                        help='input lexicon format',
                        choices=Lexicon.__members__
                        )
    args = parser.parse_args()
    main(args)
