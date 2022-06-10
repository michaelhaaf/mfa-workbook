import re
from src.models import Lexicon
from src.language import *

class Syllable:

    def __init__(self, nucleus, tone="", onset=[], coda=[]):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone

    def __eq__(self, other):
        return (isinstance(other, Syllable) and
                self.onset == other.onset and
                self.nucleus == other.nucleus and
                self.coda == other.coda and
                self.tone == other.tone)

    # TODO: which vowel does tone pair with if nucleus is long? I'll guess first
    # one (NOTE: this is wrong, revise)
    def serialize(self):
        nucleus = self.nucleus
        nucleus[0] = f"{nucleus[0] + self.tone}"
        return f"{' '.join(self.onset)} {' '.join(nucleus)} {' '.join(self.coda)}".strip()


class SyllableBuilder:

    def __init__(self, config):
        self.config = config
        self.language = config.language


    def from_phonemes(self, phonemes):
        """
        Given a list of phonemes, group them into a syllable

        Parameters
        ----------
        phonemes : iterable
            an iterable of phonemes

        Returns
        -------
        syllables : Syllable
            a Syllable object
        """
        phonemes, phonemes_with_tones = self.language.separate_tones(phonemes)
        try:
            vowel_indices = self.language.extract_vowel_indices(phonemes)
            sonorant_indices =  self.language.extract_sonorant_indices(phonemes)
            tone = self.language.extract_tone(phonemes_with_tones, vowel_indices, sonorant_indices)
            onset = self.language.extract_onset(phonemes, vowel_indices)
            nucleus, coda = self.language.extract_nucleus_coda(phonemes, vowel_indices, sonorant_indices)
        except SyllableException as ex:
            print(f"Skipping phoneme {phonemes_with_tones}: {ex}")
            return None
        return Syllable(onset=onset, nucleus=nucleus, coda=coda, tone=tone)


class SyllableException(ValueError):
    pass
