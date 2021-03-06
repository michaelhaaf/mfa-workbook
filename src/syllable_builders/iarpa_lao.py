from src.config import Config
from src.model import Syllable, Pronunciation
from src.syllable_builders.syllable_builder import SyllableBuilder


class IARPA_Lao_Builder(SyllableBuilder):

    def __init__(self, config: Config):
        self.config = config


    def from_phonemes(self, phonemes: list[str]) -> Syllable:
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
        phonemes_no_tones = super().remove_tones(phonemes)
        vowel_indices = super().extract_vowel_indices(phonemes_no_tones)
        sonorant_indices =  super().extract_sonorant_indices(phonemes_no_tones)

        tone = self.extract_tone(phonemes)
        onset = super().extract_onset(phonemes_no_tones, vowel_indices)
        nucleus, coda = super().extract_nucleus_coda(phonemes_no_tones, vowel_indices, sonorant_indices)

        return Syllable(onset=onset, nucleus=nucleus, coda=coda, tone=tone)


    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        pass


    def extract_tone(self, phonemes):
        return phonemes[-1].replace("_", "")

    def contains_vowel(self, phoneme):
        vowels = self.config.vowels
        return any(letter in vowels for letter in phoneme)
