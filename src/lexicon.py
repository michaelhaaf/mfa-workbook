from enum import Enum, auto
from dataclasses import dataclass
from src.syllable import Syllable, SyllableBuilder


class Lexicon(Enum):
    MFA = auto()
    IARPA_CANTO = auto()
    IARPA_LITHU = auto()


@dataclass
class Configuration:
    lexicon: Lexicon
    pronunciation_bound: str
    syllable_bound: str
    phoneme_bound: str
    tokens_to_remove: str  # pattern, list? different name?
    include_tones: bool


class LexiconIO:

    def __init__(self, input_config, output_config):
        self.input_config = input_config
        self.output_config = output_config

    def serialize(self, word, pronunciation):
        serialized_syllables = [syllable.serialize()
                                for syllable in pronunciation]
        output_pronunciation = self.output_config.syllable_bound.join(
            serialized_syllables)
        output_pronunciation = \
            output_pronunciation.translate(str.maketrans(
                '', '', self.output_config.tokens_to_remove))
        return (word, output_pronunciation)

    def deserialize(self, entry):
        word = entry[1]
        input_pronunciations = entry[2:]

        pronunciations = []
        for pronunciation in input_pronunciations:
            syll_phonemes = [s.split(self.input_config.phoneme_bound)
                             for s in pronunciation.split(self.input_config.syllable_bound)]

            # temp workaround
            for i, elem in enumerate(syll_phonemes):
                if len(elem) < 2 or len(elem) > 4:
                    print(
                        f"Syllable {elem} has {len(elem)} phonemes, dropping from dict")
                    syll_phonemes.pop(i)

            syllables = [SyllableBuilder.from_phonemes(phonemes)
                         for phonemes in syll_phonemes]
            pronunciations.append(syllables)

        return (word, pronunciations)
