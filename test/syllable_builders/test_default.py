import unittest
from pathlib import Path
import os
import sys

parentdir = Path(__file__).parents[2]
sys.path.append(parentdir)

from src.syllable_builders.default import Default_Builder

class Default_Builder_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        print(f"Testing {self.id()}")

    def test_test(self):
        pass

if __name__ == '__main__':
    unittest.main()
