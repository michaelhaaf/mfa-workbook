# TODO incorporate config, programmable build behavior for different languages

class Syllable:

    def __init__(self, nucleus, tone, onset="", coda=""):
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

    def serialize(self):
        return f"{self.onset} {self.nucleus}{self.tone} {self.coda}".strip()


class SyllableBuilder:

    # Input: a list of strings (each string a phoneme)
    def from_phonemes(phonemes):

        if len(phonemes) == 2:
            return Syllable(
                nucleus=phonemes[0],
                tone=phonemes[1]
            )

        elif len(phonemes) == 4:
            return Syllable(
                onset=phonemes[0],
                nucleus=phonemes[1],
                coda=phonemes[2],
                tone=phonemes[3]
            )

        elif len(phonemes) == 3:

            if _contains_vowel(phonemes[0]):
                return Syllable(
                    nucleus=phonemes[0],
                    coda=phonemes[1],
                    tone=phonemes[2]
                )

            else:
                return Syllable(
                    onset=phonemes[0],
                    nucleus=phonemes[1],
                    tone=phonemes[2]
                )

        else:
            raise SyllableException(
                f"Syllable {phonemes} has {len(phonemes)} phonemes; syllables can have 2, 3, or 4 phonemes only.")


class SyllableException(ValueError):
    pass


def _contains_vowel(phoneme):
    vowels = "aeiou"
    return any(letter in vowels for letter in phoneme)
