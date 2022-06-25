from src.config import Config
from src.model import Syllable, Pronunciation
from src.syllable_builders import SyllableBuilder


class IARPABabelCantonese(SyllableBuilder):

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
        phonemes_no_tones = self.remove_tones(phonemes)
        vowel_indices = self.language.extract_vowel_indices(phonemes_no_tones)
        sonorant_indices =  self.language.extract_sonorant_indices(phonemes_no_tones)

        tone = self.language.extract_tone(phonemes, vowel_indices, sonorant_indices)
        onset = self.language.extract_onset(phonemes_no_tones, vowel_indices)
        nucleus, coda = self.language.extract_nucleus_coda(phonemes_no_tones, vowel_indices, sonorant_indices)
        return Syllable(onset=onset, nucleus=nucleus, coda=coda, tone=tone)


    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        pass


    def extract_tone(self, phonemes, vowel_indices, sonorant_indices):
        return phonemes[-1].replace("_", "")
