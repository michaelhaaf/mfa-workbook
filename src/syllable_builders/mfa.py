import copy
from src.config import Config
from src.model import Syllable, Pronunciation
from src.syllable_builders.syllable_builder import SyllableBuilder


class MFA_Builder(SyllableBuilder):

    def _init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        pass

    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        phonemes = ""
        for syllable in pronunciation.syllables:
            nucleus = copy.copy(syllable.nucleus)
            if self.config.include_tones:
                nucleus[0] = f"{nucleus[0] + syllable.tone}"
            if syllable.onset:
                phonemes += self.config.phoneme_bound.join(syllable.onset).strip() + self.config.phoneme_bound
            phonemes += self.config.phoneme_bound.join(nucleus).strip() + self.config.phoneme_bound
            phonemes += self.config.phoneme_bound.join(syllable.coda).strip()
            phonemes = phonemes.strip()
            phonemes += self.config.syllable_bound
        return phonemes.strip()
