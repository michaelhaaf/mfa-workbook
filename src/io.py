import csv
import os
import sys

from dataclasses import dataclass
from src.model import Pronunciation
from src.config import Config


@dataclass
class Request:
    word: str
    phonemes: list[str]

@dataclass
class SyllableRequest:
    word: str
    pronunciation: Pronunciation

@dataclass
class Response:
    word: str
    pronunciation: str


class FileIO:
    def __init__(self, input_config: Config, output_config: Config):
        self.input_config = input_config
        self.output_config = output_config


    # TODO: needs refactoring
    def import_file(self, filename: str) -> list[Request]:
        with open(filename, "r") as tsvin:
            csv.register_dialect('my_dialect',
                    quoting=csv.QUOTE_NONE,
                    doublequote=False,
                    delimiter=self.input_config.pronunciation_bound)
            tsvin = csv.reader(tsvin, dialect='my_dialect')

            requests=[]
            for entry in tsvin:
                word = entry[self.input_config.word_column]
                pronunciations = entry[self.input_config.word_column+1:]

                phonemes=[]
                for p in pronunciations:
                    if self.input_config.word_bound:
                        p = p.replace(self.input_config.word_bound, self.input_config.syllable_bound)
                    phonemes = [s.split(self.input_config.phoneme_bound)
                            for s in p.split(self.input_config.syllable_bound)]
                    requests.append(Request(word, phonemes))

            return requests


    def export_file(self, output_filename: str, responses: list[Response]):
        with open(output_filename, "w") as tsvout:
            tsvout = csv.writer(tsvout, delimiter=self.output_config.pronunciation_bound)
            output_entries = [(r.word, r.pronunciation) for r in responses]
            for p in output_entries:
                tsvout.writerow(p)
