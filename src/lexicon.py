from src.syllable import Syllable, SyllableBuilder

class LexiconIO:

    def __init__(self, input_config, output_config):
        self.input_config = input_config
        self.output_config = output_config
        self.syllable_builder = SyllableBuilder(input_config)


    def serialize(self, word, pronunciation):
        """
        Given a word and its pronunciation in an input format, 
        return the word and its pronunciation transformed according
        to an output format as an conjoined entity

        Parameters
        ----------
        word : string
            a string specifying a word
        pronunciation : iterable
            a list of Syllables corresponding to the pronunciation of the word

        Returns
        -------
        (word, pronunciation) : tuple (string, string)
            the input word and the transformed pronunciation as a tuple of strings
        """
        serialized_syllables = [syllable.serialize() for syllable in pronunciation]
        output_pronunciation = self.output_config.syllable_bound.join(serialized_syllables)
        return (word, output_pronunciation)


    def deserialize(self, entry):
        """
        Given an entry in a word-pronunciation dictionary, decompose the entry into a word
        and its component Syllables.

        Parameters
        ----------
        entry : iterable 
            an entry in a pronunciation dictionary (e.g., a row in a .tsv file)

        Returns
        -------
        (word, pronunciation) : tuple (string, iterable)
            the word corresponding to the entry, and a list of syllables corresponding to its pronunciation
        """
        word = entry[self.input_config.word_column]
        input_pronunciations = entry[self.input_config.word_column+1:]
        output_pronunciations = []

        for p in input_pronunciations:
            p = p.replace(self.input_config.word_bound, self.input_config.syllable_bound)
            syll_phonemes = [s.split(self.input_config.phoneme_bound)
                             for s in p.split(self.input_config.syllable_bound)]

            syllables = (self.syllable_builder.from_phonemes(phonemes)
                    for phonemes in syll_phonemes)
            syllables = list(filter(lambda x: x is not None, syllables))
            output_pronunciations.append(syllables)

        return (word, output_pronunciations)
