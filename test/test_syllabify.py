import unittest
from pathlib import Path
import os
import sys
import csv
import itertools

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class ProcessLexiconTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(__file__)

    def test_convert_lexicon_entry_with_tones(self):
        pass
        # setup
        # sample_lexicon_path = os.path.join(
        #     self.test_dir, 'fixtures', 'sample_lexicon.txt')
        # sample_result_path = os.path.join(
        #     self.test_dir, 'fixtures', 'sample_result.txt')

        # # test & assert
        # with open(sample_lexicon_path, "r") as test_input, open(sample_result_path, "r") as expected_output:
        #     test_input = csv.reader(test_input, delimiter='\t')
        #     expected_output = csv.reader(expected_output, delimiter='\t')

        #     for (input_element, expected_result) in zip(test_input, expected_output):
        #         test_result = convert_lexicon_element(input_element)
        #         self.assertEqual(test_result, expected_result)


    def test_convert_lexicon_entry_without_tones(self):
        pass
        # setup
        # sample_lexicon_path = os.path.join(
        #     self.test_dir, 'fixtures', 'sample_lexicon.txt')
        # sample_result_path = os.path.join(
        #     self.test_dir, 'fixtures', 'sample_result_no_tones.txt')

        # # test & assert
        # with open(sample_lexicon_path, "r") as test_input, open(sample_result_path, "r") as expected_output:
        #     test_input = csv.reader(test_input, delimiter='\t')
        #     expected_output = csv.reader(expected_output, delimiter='\t')

        #     for (input_element, expected_result) in zip(test_input, expected_output):
        #         test_result = convert_lexicon_element(input_element, use_tones=False)
        #         self.assertEqual(test_result, expected_result)
