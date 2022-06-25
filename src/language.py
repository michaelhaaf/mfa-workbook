
class Language:

    def separate_tones(self, phonemes):
        phonemes_no_tones = list(map(lambda x: re.sub(self.config.tone_characters, '', x), phonemes))
        phonemes_no_tones = [x for x in phonemes_no_tones if x]
        return phonemes_no_tones, phonemes


    def extract_vowel_indices(self, phonemes):
        indices = [i for i, x in enumerate(map(self.contains_vowel, phonemes)) if x]
        if not indices:
            raise SyllableException("Cannot process phoneme without vowels.")
        return indices


    def extract_sonorant_indices(self, phonemes):
        return [i for i, x in enumerate(map(self.contains_sonorant, phonemes)) if x]


    def extract_tone(self, phonemes, vowel_indices, sonorant_indices):
        tone = ""
        if not self.config.include_tones:
            tone = ""
        elif self.config.lexicon == Lexicon.IARPA_CANTO:
            tone = self._extract_canto_tone(phonemes)
        elif self.config.lexicon == Lexicon.IARPA_LITHU:
            tone = self._extract_lithu_tone(phonemes, vowel_indices, sonorant_indices)
        return tone


    def extract_canto_tone(self, phonemes):
        return phonemes[-1].replace("_", "")


    def extract_onset(self, phonemes, vowel_indices):
        return phonemes[0:vowel_indices[0]]


    def extract_nucleus_coda(self, phonemes, vowel_indices, sonorant_indices):
        if self._is_long_vowel(vowel_indices, sonorant_indices):
            nucleus = phonemes[vowel_indices[0]:vowel_indices[0]+2]
            coda = phonemes[vowel_indices[0]+2:]
            return nucleus, coda
        else:
            nucleus = [phonemes[vowel_indices[0]]]
            coda = phonemes[vowel_indices[0]+1:]
            return nucleus, coda


    def is_vowel_sequence(self, vowel_indices):
        return len(vowel_indices) > 1 and vowel_indices[1] - vowel_indices[0] == 1


    def is_sonorant(self, vowel_indices, sonorant_indices):
        return len(sonorant_indices) > 0 and sonorant_indices[0] - vowel_indices[0] == 1


    def is_long_vowel(self, vowel_indices, sonorant_indices):
        return self._is_vowel_sequence(vowel_indices) or self._is_sonorant(vowel_indices, sonorant_indices)


    def contains_sonorant(self, phoneme):
        sonorants = self.config.sonorants
        return any(letter.lower() in sonorants for letter in phoneme)


    def contains_vowel(self, phoneme):
        vowels = self.config.vowels
        return any(letter.lower() in vowels for letter in phoneme) and phoneme[0] != "_"


# TODO: inherit language as an interface so that all languages must implement
#       common methods
class Lithuanian:

    def extract_tone(self, phonemes, vowel_indices, sonorant_indices):
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

class Cantonese:
    def extract_tone(self, phonemes, vowel_indices, sonorant_indices):
        
