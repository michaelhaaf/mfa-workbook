import re
from src.config import Config
from src.model import Syllable, Pronunciation


class SyllableBuilderInterface:

    def __init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        pass

    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        pass


class SyllableBuilder(SyllableBuilderInterface):
    """ Abstract class containing common helper hethods to be inherited by subclasses"""

    def __init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        pass

    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        pass


    def contains_vowel(self, phoneme):
        vowels = self.config.vowels
        return any(letter.lower() in vowels for letter in phoneme)

    def contains_sonorant(self, phoneme):
        sonorants = self.config.sonorants
        return any(letter.lower() in sonorants for letter in phoneme)

    def is_vowel_sequence(self, vowel_indices):
        return len(vowel_indices) > 1 and vowel_indices[1] - vowel_indices[0] == 1

    def is_sonorant(self, vowel_indices, sonorant_indices):
        return len(sonorant_indices) > 0 and sonorant_indices[0] - vowel_indices[0] == 1

    def is_long_vowel(self, vowel_indices, sonorant_indices):
        return self.is_vowel_sequence(vowel_indices) or self.is_sonorant(vowel_indices, sonorant_indices)

    def remove_tones(self, phonemes):
        phonemes_no_tones = list(map(lambda x: re.sub(self.config.tone_characters, '', x), phonemes))
        phonemes_no_tones = [x for x in phonemes_no_tones if x]
        return phonemes_no_tones

    def extract_vowel_indices(self, phonemes):
        indices = [i for i, x in enumerate(map(self.contains_vowel, phonemes)) if x]
        if not indices:
            raise SyllableBuilderException(f"Syllable phonemes {phonemes} contain no vowels.")
        return indices

    def extract_sonorant_indices(self, phonemes):
        return [i for i, x in enumerate(map(self.contains_sonorant, phonemes)) if x]

    def extract_onset(self, phonemes, vowel_indices):
        return phonemes[0:vowel_indices[0]]

    def extract_nucleus_coda(self, phonemes, vowel_indices, sonorant_indices):
        if self.is_long_vowel(vowel_indices, sonorant_indices):
            nucleus = phonemes[vowel_indices[0]:vowel_indices[0]+2]
            coda = phonemes[vowel_indices[0]+2:]
            return nucleus, coda
        else:
            nucleus = [phonemes[vowel_indices[0]]]
            coda = phonemes[vowel_indices[0]+1:]
            return nucleus, coda

class SyllableBuilderException(ValueError):
    pass
