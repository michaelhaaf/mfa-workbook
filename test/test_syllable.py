import unittest
from pathlib import Path
import os
import sys

from src.syllable import SyllableBuilder, Syllable

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class SyllableTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(__file__)

    def test_serialize_two_phoneme_syllable(self):

        # setup
        two_phoneme_syllable = Syllable(nucleus="m", tone="_4")

        # test
        expectation = "m_4"
        result = two_phoneme_syllable.serialize()

        # assert
        self.assertEqual(result, expectation)

    def test_serialize_four_phoneme_syllable(self):

        # setup
        four_phoneme_syllable = Syllable(
            onset="s", nucleus="i:", coda="n", tone="_1")

        # test
        expectation = "s i:_1 n"
        result = four_phoneme_syllable.serialize()

        # assert
        self.assertEqual(result, expectation)

    def test_serialize_three_phoneme_syllable_no_onset(self):

        # setup
        three_phoneme_syllable = Syllable(nucleus="a:", coda="p", tone="_3")

        # test
        expectation = "a:_3 p"
        result = three_phoneme_syllable.serialize()

        # assert
        self.assertEqual(result, expectation)

    def test_serialize_three_phoneme_syllable_no_coda(self):

        # setup
        three_phoneme_syllable = Syllable(onset="b", nucleus="a:w", tone="_1")

        # test
        expectation = "b a:w_1"
        result = three_phoneme_syllable.serialize()

        # assert
        self.assertEqual(result, expectation)


class SyllableBuilderTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(__file__)

    def test_from_phonemes_two_phonemes_makes_syllable_with_order_nucleus_tone(self):

        # setup
        two_phonemes = "m _4".split(" ")

        # test
        expectation = Syllable(nucleus="m", tone="_4")
        result = SyllableBuilder.from_phonemes(two_phonemes)

        # assert
        self.assertEqual(result, expectation)

    def test_from_phonemes_four_phonemes_makes_syllable_with_order_onset_nucleus_coda_tone(self):

        # setup
        four_phonemes = "s i: n _1".split(" ")

        # test
        expectation = Syllable(onset="s", nucleus="i:", coda="n", tone="_1")
        result = SyllableBuilder.from_phonemes(four_phonemes)

        # assert
        self.assertEqual(result, expectation)

    def test_from_phonemes_three_phonemes_vowel_first_makes_syllable_with_order_nucleus_coda_tone(self):

        # setup
        three_phonemes = "a: p _3".split(" ")

        # test
        expectation = Syllable(nucleus="a:", coda="p", tone="_3")
        result = SyllableBuilder.from_phonemes(three_phonemes)

        # assert
        self.assertEqual(result, expectation)

    def test_from_phonemes_three_phonemes_vowel_second_makes_syllable_with_order_onset_nucleus_tone(self):

        # setup
        three_phonemes = "b a:w _1".split(" ")

        # test
        expectation = Syllable(onset="b", nucleus="a:w", tone="_1")
        result = SyllableBuilder.from_phonemes(three_phonemes)

        # assert
        self.assertEqual(result, expectation)

    def test_from_phonemes_three_phonemes_no_vowel_makes_syllable_with_order_onset_nucleus_tone(self):

        # setup
        # NOTE: "6w" is probably in fact a vowel
        three_phonemes = "g 6w _2".split(" ")

        # test
        expectation = Syllable(onset="g", nucleus="6w", tone="_2")
        result = SyllableBuilder.from_phonemes(three_phonemes)

        # assert
        self.assertEqual(result, expectation)


if __name__ == '__main__':
    unittest.main()
