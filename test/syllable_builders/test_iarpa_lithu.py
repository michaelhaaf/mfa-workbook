import unittest
from pathlib import Path
import os
import sys
import dataclasses

parentdir = Path(__file__).parents[2]
sys.path.append(parentdir)
from src.syllable_builders.iarpa_lithu import IARPA_Lithu_Builder
from src.model import Syllable, Pronunciation
from src.config import Config


class IARPA_Lithu_Builder_test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        print("Testing src.syllable_builders.iarpa_lithu IARPA_Lithu_Builder:")

    @classmethod
    def tearDownClass(cls):
        print("Finished testing src.syllable_builders.iarpa_lithu IARPA_Lithu_Builder")
        pass


    def setUp(self):
        self.iarpa_lithu_config = Config(
                pronunciation_bound="\t",
                word_bound=" # ",
                syllable_bound=" . ",
                phoneme_bound=" ",
                word_column=0,
                tone_characters='"|_R|_F',
                include_tones=True,
                sonorants="rlmn",
                vowels="aAE{eiIoOUu")
        self.iarpa_lithu_builder = IARPA_Lithu_Builder(self.iarpa_lithu_config)

    def tearDown(self):
        pass


    def test_dipthong_is_heavy_syllable(self):
        # setup
        syllable_with_diphthong = ["b'", "E", "I_R"]

        # test
        expectation = True
        result = self.iarpa_lithu_builder.is_heavy_syllable(syllable_with_diphthong)

        # assert
        self.assertEqual(result, expectation)


    def test_sonorant_is_heavy_syllable(self):
        # setup
        syllable_with_sonorant = ["p'", "a", "n"]

        # test
        expectation = True
        result = self.iarpa_lithu_builder.is_heavy_syllable(syllable_with_sonorant)

        # assert
        self.assertEqual(result, expectation)


    def test_long_vowel_is_heavy_syllable(self):
        # setup
        syllable_with_long_vowel = ["p'", "A:"]

        # test
        expectation = True
        result = self.iarpa_lithu_builder.is_heavy_syllable(syllable_with_long_vowel)

        # assert
        self.assertEqual(result, expectation)


    def test_default_vowel_is_light_syllable(self):

        # setup
        syllable_with_default_vowel = ["p'", "a", "s"]

        # test
        expectation = False
        result = self.iarpa_lithu_builder.is_heavy_syllable(syllable_with_default_vowel)

        # assert
        self.assertEqual(result, expectation)


    def test_unstressed_light_syllable_has_tone_1(self):

        # setup
        unstressed_light_syllable = ["p'", "a", "s"]

        # test
        expectation = Syllable(nucleus=["a"], tone="1", onset=["p'"], coda=["s"])
        result = self.iarpa_lithu_builder.from_phonemes(unstressed_light_syllable)

        # assert
        self.assertEqual(result, expectation)


    def test_stressed_light_syllable_has_tone_2(self):

        # setup
        # žuvo	" Z U . v o:
        stressed_light_syllable = ['"', "Z", "U"]

        # test
        expectation = Syllable(nucleus=["U"], tone="2", onset=["Z"], coda=[])
        result = self.iarpa_lithu_builder.from_phonemes(stressed_light_syllable)

        # assert
        self.assertEqual(result, expectation)


    def test_unstressed_heavy_syllable_has_tone_3(self):

        # setup
        # žuvo	" Z U . v o:
        unstressed_heavy_syllable = ["v", "o:"]

        # test
        expectation = Syllable(nucleus=["o:"], tone="3", onset=["v"], coda=[])
        result = self.iarpa_lithu_builder.from_phonemes(unstressed_heavy_syllable)

        # assert
        self.assertEqual(result, expectation)


    def test_stressed_rising_heavy_syllable_has_tone_4(self):

        # setup
        # žymiai	" Z' i:_R . m' a I
        stressed_rising_heavy_syllable = ['"', "Z'", "i:_R"]

        # test
        expectation = Syllable(nucleus=["i:"], tone="4", onset=["Z'"], coda=[])
        result = self.iarpa_lithu_builder.from_phonemes(stressed_rising_heavy_syllable)

        # assert
        self.assertEqual(result, expectation)


    def test_stressed_falling_heavy_syllable_has_tone_5(self):

        # setup
        # žymiausias	Z' i: . " m' a_F U . s' a s
        stressed_falling_heavy_syllable = ['"', "m'", "a_F", "U"]

        # test
        expectation = Syllable(nucleus=["a","U"], tone="5", onset=["m'"], coda=[])
        result = self.iarpa_lithu_builder.from_phonemes(stressed_falling_heavy_syllable)

        # assert
        self.assertEqual(result, expectation)


if __name__ == '__main__':
    unittest.main()
