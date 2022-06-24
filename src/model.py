class Pronunciation:
    def __init__(self, syllables: list[Syllable]):
        self.syllables = syllables

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
