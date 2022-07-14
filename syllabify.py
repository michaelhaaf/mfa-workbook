#!/usr/bin/env python3

import argparse
import csv
import os
import sys
import yaml
import dacite

from src.corpus import Corpus, CorpusEnum, CorpusFactory
from src.io import FileIO, Request, SyllableRequest
from src.config import Config
from src.logger import logger, console_handler
from enum import Enum


def parse_input(format):
    if not format:
        return "default.yaml", CorpusEnum.DEFAULT.name

    config_filename, corpus_name = "", ""
    if format.upper() in CorpusEnum.__members__:
        corpus_name = format.upper()
    else:
        corpus_name = CorpusEnum.DEFAULT.name

    if f"{format.lower()}.yaml" in os.listdir("./config"):
        config_filename = format.lower()
    else:
        config_filename = CorpusEnum.DEFAULT.name.lower()

    return config_filename, corpus_name


# TODO: might not need dacite afterall
def load_configs(input_format, output_format):
    with open(f"config/{input_format}.yaml", "r") as input_config, open(f"config/{output_format}.yaml", "r") as output_config:
        output_config = dacite.from_dict(
                data_class=Config,
                data=yaml.safe_load(output_config),
                config=dacite.Config()
                )
        input_config = dacite.from_dict(
                data_class=Config,
                data=yaml.safe_load(input_config),
                config=dacite.Config()
                )
        return input_config, output_config


def main(args):

    config_filename, corpus_name = parse_input(args.format)
    logger.addHandler(console_handler)
    logger.info(f"Using config file {config_filename}.yaml and corpus {corpus_name}...")

    input_config, output_config = load_configs(config_filename, CorpusEnum.MFA.name.lower())
    input_corpus = CorpusFactory(input_config).create(corpus_name)
    output_corpus = CorpusFactory(output_config).create(CorpusEnum.MFA.name.upper())
    fileio = FileIO(input_config, output_config)

    requests = fileio.import_file(args.input_lexicon)
    syllable_requests = filter(None, (input_corpus.syllabify(r) for r in requests))
    responses = [output_corpus.desyllabify(r) for r in syllable_requests]
    fileio.export_file(args.output_dict, responses)
    logger.info(f"Syllabification complete. See {args.output_dict} for output, and syllabify.log for any debug/error messages.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Convert lexicon of specified format and language to MFA pronunciation dictionary')
    parser.add_argument('-i',
                        required=True,
                        help='lexicon txt file',
                        type=str,
                        dest='input_lexicon'
                        )
    parser.add_argument('-o',
                        required=True,
                        help='mfa-ready output destination',
                        type=str,
                        dest='output_dict'
                        )
    parser.add_argument('-f',
                        required=False,
                        dest='format',
                        help=f"Available options (case insensitive): {[corpus for corpus in CorpusEnum.__members__]}. If no format specified, DEFAULT is used",
                        type=str
                        )
    args = parser.parse_args()
    main(args)
