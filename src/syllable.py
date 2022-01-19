class Syllable:

    def __init__(self, nucleus, tone, onset="", coda=""):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone

    def serialize(self, use_tones=True):
        serializer = get_serializer(use_tones)
        return serializer(self)

    def __eq__(self, other):
        return (isinstance(other, Syllable) and
                self.onset == other.onset and
                self.nucleus == other.nucleus and
                self.coda == other.coda and
                self.tone == other.tone)


def get_serializer(use_tones):
    if use_tones:
        return _serialize_with_tones
    else:
        return _serialize_without_tones


def _serialize_with_tones(syllable):
    return f"{syllable.onset} {syllable.nucleus}{syllable.tone} {syllable.coda}".strip()


def _serialize_without_tones(syllable):
    return f"{syllable.onset} {syllable.nucleus} {syllable.coda}".strip()


def contains_vowel(phoneme):
    vowels = "aeiou"
    return any(letter in vowels for letter in phoneme)


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

            if contains_vowel(phonemes[0]):
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
            raise SyllableException("Syllable can have 2, 3, or 4 phonemes only.")


class SyllableException(ValueError):
    pass
