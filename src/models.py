from enum import Enum, auto
from dataclasses import dataclass

class Lexicon(Enum):
    MFA = auto()
    IARPA_CANTO = auto()
    IARPA_LITHU = auto()


@dataclass
class Configuration:
    lexicon: Lexicon
    word_bound: str
    pronunciation_bound: str
    syllable_bound: str
    phoneme_bound: str
    word_column: int
    tone_characters: str
    include_tones: bool
    sonorants: str
    vowels: str
