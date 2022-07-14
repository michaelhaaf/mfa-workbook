from src.config import Config
from src.model import Syllable, Pronunciation
from src.syllable_builders.syllable_builder import SyllableBuilder, SyllableBuilderException


class IARPA_Canto_Builder(SyllableBuilder):

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
        vowel_indices = self.extract_vowel_indices(phonemes_no_tones)
        sonorant_indices =  super().extract_sonorant_indices(phonemes_no_tones)

        tone = self.extract_tone(phonemes)
        onset = super().extract_onset(phonemes_no_tones, vowel_indices)
        nucleus, coda = super().extract_nucleus_coda(phonemes_no_tones, vowel_indices, sonorant_indices)

        return Syllable(onset=onset, nucleus=nucleus, coda=coda, tone=tone)


    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        pass


    def extract_tone(self, phonemes):
        return phonemes[-1].replace("_", "")

    def extract_vowel_indices(self, phonemes):
        indices = [i for i, x in enumerate(map(self.contains_vowel, phonemes)) if x]
        if not indices:
            if phonemes[0].lower() in ('m', 'n'):
                indices = [0]
            else:
                raise SyllableBuilderException(f"Syllable phonemes {phonemes} contain no vowels.")
        return indices

