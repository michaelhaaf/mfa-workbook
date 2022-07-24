import unittest
from pathlib import Path
import os
import sys
import dataclasses

parentdir = Path(__file__).parents[2]
sys.path.append(parentdir)
from src.syllable_builders.iarpa_lao import IARPA_Lao_Builder
from src.model import Syllable, Pronunciation
from src.config import Config


class IARPA_Lao_Builder_test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        self.iarpa_lao_config = Config(
                pronunciation_bound="\t",
                word_bound=" # ",
                syllable_bound=" . ",
                phoneme_bound=" ",
                word_column=0,
                tone_characters='_[0-6]',
                include_tones=True,
                sonorants="",
                vowels="ieEAMu7o0")
        self.iarpa_lao_builder = IARPA_Lao_Builder(self.iarpa_lao_config)

    def tearDown(self):
        pass


    def test_tone_parsed_explicitly(self):
        # setup
        syllable_with_tone = ["k", "u@", "t", "_6"]

        # test
        expectation = Syllable(nucleus=["u@"], tone="6", onset=["k"], coda=["t"])
        result = self.iarpa_lao_builder.from_phonemes(syllable_with_tone)

        # assert
        self.assertEqual(result, expectation)

