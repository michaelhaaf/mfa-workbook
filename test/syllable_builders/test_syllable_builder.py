import unittest
from pathlib import Path
import os
import sys

parentdir = Path(__file__).parents[2]
sys.path.append(parentdir)
from src.syllable_builders.syllable_builder import SyllableBuilder


class SyllableBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Testing src.syllable_builders.syllable_builder SyllableBuilder:")

    @classmethod
    def tearDownClass(cls):
        print("Finished testing src.syllable_builders.syllable_builder SyllableBuilder")
        pass

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
