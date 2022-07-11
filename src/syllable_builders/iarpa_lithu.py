from src.config import Config
from src.model import Syllable, Pronunciation
from src.syllable_builders.syllable_builder import SyllableBuilder


class IARPA_Lithu_Builder(SyllableBuilder):

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
        tone = ""
        if self.is_heavy_syllable(phonemes):
            if len([s for s in phonemes if '_R' in s]) > 0:
                tone = "4"
            elif len([s for s in phonemes if '_F' in s]) > 0:
                tone = "5"
            else:
                tone = "3"
        else:
            if phonemes[0] == '"':
                tone = "2"
            else:
                tone = "1"
        return tone


    def is_heavy_syllable(self, phonemes):
        phonemes_no_tones = super().remove_tones(phonemes)
        vowel_indices = super().extract_vowel_indices(phonemes_no_tones)
        sonorant_indices =  super().extract_sonorant_indices(phonemes_no_tones)
        return (
                super().is_vowel_sequence(vowel_indices) or
                super().is_sonorant(vowel_indices, sonorant_indices) or
                any(":" in p for p in phonemes)
        )
