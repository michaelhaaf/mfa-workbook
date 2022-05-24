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

from src.lexicon import LexiconIO
from src.models import Lexicon, Configuration


def load_config(format):
    with open(f"config/{format}.yaml", "r") as input_config, open("config/mfa.yaml", "r") as output_config:
        converters = {Lexicon: lambda x: Lexicon[x]}
        output_config = dacite.from_dict(
                data_class=Configuration,
                data=yaml.safe_load(output_config),
                config=dacite.Config(type_hooks=converters)
                )
        input_config = dacite.from_dict(
                data_class=Configuration,
                data=yaml.safe_load(input_config),
                config=dacite.Config(type_hooks=converters)
                )
        return input_config, output_config


def main(args):

    input_config, output_config = load_config(args.format.lower())
    lexiconIO = LexiconIO(input_config=input_config,
                          output_config=output_config)

    with open(args.lexicon, "r") as tsvin, open(args.output_dict, "w") as tsvout:
        csv.register_dialect('my_dialect',
                quoting=csv.QUOTE_NONE,
                doublequote=False,
                delimiter=input_config.pronunciation_bound)

        tsvin = csv.reader(tsvin, dialect='my_dialect')
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
