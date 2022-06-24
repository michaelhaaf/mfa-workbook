from dataclasses import dataclass

# TODO: use enum again for mapping config to syllable builder
@dataclass
class Config:
    pronunciation_bound: str
    word_bound: str
    syllable_bound: str
    phoneme_bound: str
    word_column: int
    tone_characters: str
    sonorants: str
    vowels: str
    include_tones: bool
