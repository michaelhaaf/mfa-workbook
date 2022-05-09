import re
from src.models import Lexicon

class Syllable:

    def __init__(self, nucleus, tone="", onset=[], coda=[]):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone

    def __eq__(self, other):
        return (isinstance(other, Syllable) and
                self.onset == other.onset and
                self.nucleus == other.nucleus and
                self.coda == other.coda and
                self.tone == other.tone)

    # TODO: which vowel does tone pair with if nucleus is long? I'll guess first
    # one
    def serialize(self):
        nucleus = self.nucleus
        nucleus[0] = f"{nucleus[0] + self.tone}"
        return f"{' '.join(self.onset)} {' '.join(nucleus)} {' '.join(self.coda)}".strip()


class SyllableBuilder:

    def __init__(self, config):
        self.config = config

    def from_phonemes(self, phonemes):
        phonemes, phonemes_withtones = self._separate_tones(phonemes)
        try:
            vowel_indices = self._extract_vowel_indices(phonemes)
            sonorant_indices =  self._extract_sonorant_indices(phonemes)

            tone = self._extract_tone(phonemes_withtones, vowel_indices, sonorant_indices)
            onset = self._extract_onset(phonemes, vowel_indices)
            nucleus, coda = self._extract_nucleus_coda(phonemes, vowel_indices, sonorant_indices)
        except SyllableException as ex:
            print(f"Skipping phoneme {phonemes_withtones}: {ex}")
            return None
        return Syllable(onset=onset, nucleus=nucleus, coda=coda, tone=tone)


    def _separate_tones(self, phonemes):
        phonemes_notones = \
                list(map(lambda x: re.sub(self.config.tone_characters, '', x), phonemes))
        phonemes_notones = [x for x in phonemes_notones if x]
        return phonemes_notones, phonemes


    def _extract_vowel_indices(self, phonemes):
        indices = [i for i, x in enumerate(map(self._contains_vowel, phonemes)) if x]
        if not indices:
            raise SyllableException("Cannot process phoneme without vowels.")
        return indices


    def _extract_sonorant_indices(self, phonemes):
        return [i for i, x in enumerate(map(self._contains_sonorant, phonemes)) if x]


    def _extract_tone(self, phonemes, vowel_indices, sonorant_indices):
        tone = ""
        if not self.config.include_tones:
            return tone
        elif self.config.lexicon == Lexicon.IARPA_CANTO:
            tone = self._extract_canto_tone(phonemes)
        elif self.config.lexicon == Lexicon.IARPA_LITHU:
            tone = self._extract_lithu_tone(phonemes, vowel_indices, sonorant_indices)
        return tone


    def _extract_lithu_tone(self, phonemes, vowel_indices, sonorant_indices):
        tone = ""
        if self._is_long_vowel(vowel_indices, sonorant_indices):
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


    def _extract_canto_tone(self, phonemes):
        return phonemes[-1].replace("_", "")


    def _extract_onset(self, phonemes, vowel_indices):
        return phonemes[0:vowel_indices[0]]


    def _extract_nucleus_coda(self, phonemes, vowel_indices, sonorant_indices):
        if self._is_long_vowel(vowel_indices, sonorant_indices):
            nucleus = phonemes[vowel_indices[0]:vowel_indices[0]+2]
            coda = phonemes[vowel_indices[0]+2:]
            return nucleus, coda
        else:
            nucleus = [phonemes[vowel_indices[0]]]
            coda = phonemes[vowel_indices[0]+1:]
            return nucleus, coda


    def _is_vowel_sequence(self, vowel_indices):
        return len(vowel_indices) > 1 and vowel_indices[1] - vowel_indices[0] == 1


    def _is_sonorant(self, vowel_indices, sonorant_indices):
        return len(sonorant_indices) > 0 and sonorant_indices[0] - vowel_indices[0] == 1


    def _is_long_vowel(self, vowel_indices, sonorant_indices):
        return self._is_vowel_sequence(vowel_indices) or self._is_sonorant(vowel_indices, sonorant_indices)


    def _contains_sonorant(self, phoneme):
        sonorants = self.config.sonorants
        return any(letter.lower() in sonorants for letter in phoneme)


    def _contains_vowel(self, phoneme):
        vowels = self.config.vowels
        return any(letter.lower() in vowels for letter in phoneme) and phoneme[0] != "_"


class SyllableException(ValueError):
    pass
