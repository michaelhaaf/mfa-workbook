from src.config import Config
from src.model import Syllable


class SyllableBuilder:

    def __init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        """Return a Syllable object parsed from the input string"""
        pass


class IARPABabelLithuanian(SyllableBuilder):

    def __init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        """Return a Syllable object parsed from the input string"""
        pass


class IARPABabelCantonese(SyllableBuilder):

    def __init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        """Return a Syllable object parsed from the input string"""
        pass
