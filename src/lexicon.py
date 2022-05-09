from src.syllable import Syllable, SyllableBuilder

class LexiconIO:

    def __init__(self, input_config, output_config):
        self.input_config = input_config
        self.output_config = output_config
        self.syllable_builder = SyllableBuilder(input_config)

    def serialize(self, word, pronunciation):
        serialized_syllables = [syllable.serialize() for syllable in pronunciation]
        output_pronunciation = self.output_config.syllable_bound.join(
            serialized_syllables)
        return (word, output_pronunciation)

    def deserialize(self, entry):
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
