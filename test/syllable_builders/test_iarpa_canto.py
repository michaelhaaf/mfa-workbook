import unittest
from pathlib import Path
import os
import sys
import dataclasses

parentdir = Path(__file__).parents[2]
sys.path.append(parentdir)
from src.syllable_builders.iarpa_canto import IARPA_Canto_Builder
from src.model import Syllable, Pronunciation
from src.config import Config


class IARPA_Canto_Builder_test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        self.iarpa_canto_config = Config(
                pronunciation_bound="\t",
                word_bound="",
                syllable_bound=" . ",
                phoneme_bound=" ",
                word_column=1,
                tone_characters='_[0-9]',
                include_tones=True,
                sonorants="",
                vowels="aeoiuy69")
        self.iarpa_canto_builder = IARPA_Canto_Builder(self.iarpa_canto_config)

    def tearDown(self):
        pass


    def test_tone_parsed_explicitly(self):
        # setup
        syllable_with_tone = ["ts", "6j", "_4"]

        # test
        expectation = Syllable(nucleus=["6j"], tone="4", onset=["ts"])
        result = self.iarpa_canto_builder.from_phonemes(syllable_with_tone)

        # assert
        self.assertEqual(result, expectation)

    # TODO: test vowels correctly (N and M)

    # TODO: check other oddities in the corpus readme just in case

if __name__ == '__main__':
    unittest.main()
