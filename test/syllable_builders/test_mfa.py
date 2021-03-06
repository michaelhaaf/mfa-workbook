import unittest
from pathlib import Path
import os
import sys
import dataclasses

parentdir = Path(__file__).parents[2]
sys.path.append(parentdir)
from src.syllable_builders.mfa import MFA_Builder
from src.model import Syllable, Pronunciation
from src.config import Config


class MFA_Builder_test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        self.mfa_config = Config(
                pronunciation_bound="\t",
                word_bound="",
                syllable_bound=" ",
                phoneme_bound=" ",
                word_column=0,
                tone_characters="",
                include_tones=True,
                sonorants="",
                vowels="")
        self.mfa_config_no_tones = dataclasses.replace(self.mfa_config, include_tones=False)

        self.mfa_builder = MFA_Builder(self.mfa_config)
        self.mfa_builder_no_tones = MFA_Builder(self.mfa_config_no_tones)


    def tearDown(self):
        pass


    def test_to_phonemes_only_nucleus(self):

        # setup
        nucleus_syllable = Syllable(nucleus=["a:j"])
        test_pronunciation = Pronunciation(syllables=[nucleus_syllable])

        # test
        expectation = "a:j"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "a:j"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_nucleus_tone(self):

        # setup
        nucleus_tone_syllable = Syllable(nucleus=["a:j"], tone="1")
        test_pronunciation = Pronunciation(syllables=[nucleus_tone_syllable])

        # test
        expectation = "a:j1"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "a:j"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_onset_nucleus(self):

        # setup
        onset_nucleus_syllable = Syllable(onset=["g"], nucleus=["a:"])
        test_pronunciation = Pronunciation(syllables=[onset_nucleus_syllable])

        # test
        expectation = "g a:"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "g a:"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_onset_nucleus_tone(self):

        # setup
        onset_nucleus_tone_syllable = Syllable(onset=["g"], nucleus=["a:"], tone="3")
        test_pronunciation = Pronunciation(syllables=[onset_nucleus_tone_syllable])

        # test
        expectation = "g a:3"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "g a:"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_nucleus_coda(self):
        # setup
        nucleus_coda_syllable = Syllable(nucleus=["E:"], coda=["m"])
        test_pronunciation = Pronunciation(syllables=[nucleus_coda_syllable])

        # test
        expectation = "E: m"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "E: m"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_nucleus_tone_coda(self):
        # setup
        nucleus_tone_coda_syllable = Syllable(nucleus=["E:"], coda=["m"], tone="1")
        test_pronunciation = Pronunciation(syllables=[nucleus_tone_coda_syllable])

        # test
        expectation = "E:1 m"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "E: m"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_onset_nucleus_coda(self):
        # setup
        onset_nucleus_coda_syllable = Syllable(onset=["ts"], nucleus=["6"], coda=["t"])
        test_pronunciation = Pronunciation(syllables=[onset_nucleus_coda_syllable])

        # test
        expectation = "ts 6 t"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "ts 6 t"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_onset_nucleus_tone_coda(self):
        # setup
        onset_nucleus_tone_coda_syllable = Syllable(onset=["ts"], nucleus=["6"], coda=["t"], tone="1")
        test_pronunciation = Pronunciation(syllables=[onset_nucleus_tone_coda_syllable])

        # test
        expectation = "ts 61 t"
        result = self.mfa_builder.to_phonemes(test_pronunciation)
        no_tones_expectation = "ts 6 t"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(test_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_to_phonemes_pronunciation_syllables_separation(self):

        # setup
        multiple_syllables = [
                Syllable(onset=["d"], nucleus=["9y"], tone="6"),
                Syllable(onset=["dz"], nucleus=["9:"], coda=["N"], tone="2")]
        multiple_syllable_pronunciation = Pronunciation(syllables=multiple_syllables)

        # test
        expectation = "d 9y6 dz 9:2 N"
        result = self.mfa_builder.to_phonemes(multiple_syllable_pronunciation)
        no_tones_expectation = "d 9y dz 9: N"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(multiple_syllable_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


    def test_tone_bound_to_end_of_nucleus(self):

        # setup
        # corpus entry: a U k . " S t A:_R . d v a . r' I s
        # desired MFA output: aU3 k S t A:2 d v a1 r' I1 s
        aukstadvaris_syllables = [
                Syllable(nucleus=["a", "U"], coda=["k"], tone="3"),
                Syllable(onset=["S", "t"], nucleus=["A:"], tone="2"),
                Syllable(onset=["d", "v"], nucleus=["a"], tone="1"),
                Syllable(onset=["r'"], nucleus=["I"], coda=["s"], tone="1")
                ]
        aukstadvaris_pronunciation = Pronunciation(syllables=aukstadvaris_syllables)

        # test
        expectation = "aU3 k S t A:2 d v a1 r' I1 s"
        result = self.mfa_builder.to_phonemes(aukstadvaris_pronunciation)
        no_tones_expectation = "aU k S t A: d v a r' I s"
        no_tones_result = self.mfa_builder_no_tones.to_phonemes(aukstadvaris_pronunciation)

        # assert
        self.assertEqual(result, expectation)
        self.assertEqual(no_tones_result, no_tones_expectation)


if __name__ == '__main__':
    unittest.main()
