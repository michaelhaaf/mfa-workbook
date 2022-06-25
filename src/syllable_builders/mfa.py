from src.config import Config
from src.model import Syllable, Pronunciation
from src.syllable_builders import SyllableBuilder


class MFA(SyllableBuilder):

    def _init__(self, config: Config):
        self.config = config

    def from_phonemes(self, phonemes: list[str]) -> Syllable:
        pass

    def to_phonemes(self, pronunciation: Pronunciation) -> str:
        phonemes = ""
        for syllable in pronunciation:
            nucleus = syllable.nucleus
            nucleus[0] = f"{nucleus[0] + syllable.tone}"
            pronunciation += config.phoneme_bound.join(syllable.onset) + config.phoneme_bound
            pronunciation += config.phoneme_bound.join(nucleus) + config.phoneme_bound
            pronunciation += config.phoneme_bound.join(syllable.coda)
            pronunciation += config.syllable_bound
        return phonemes
