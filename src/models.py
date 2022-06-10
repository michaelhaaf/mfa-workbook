from enum import Enum, auto
from dataclasses import dataclass
from src.language import Language

class Lexicon(Enum):
    MFA = auto()
    IARPA_CANTO = auto()
    IARPA_LITHU = auto()


@dataclass
class Configuration:
    lexicon: Lexicon
    language: Language
    include_tones: bool
    word_bound: str
    pronunciation_bound: str
    syllable_bound: str
    phoneme_bound: str
    word_column: int
    tone_characters: str
    sonorants: str
    vowels: str
