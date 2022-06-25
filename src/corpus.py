from src.config import Config
from src.io import Request, SyllableRequest, Response
from src.syllableBuilder import SyllableBuilder


class Corpus:

    def __init__(self, syllable_builder: SyllableBuilder):
        self.syllable_builder = syllable_builder


    def syllabify(self, request: Request) -> SyllableRequest:
        """
        Given a word and its phoneme set (a Request object),
        return the word and its pronunciation (a SyllableRequest
        object) transformed to an output format specified by the Config object.
        """
        syllables = [self.syllable_builder.from_phonemes(request.phonemes)]
        pronunciation = Pronunciation(syllables)
        return SyllableRequest(request.word, pronunciation)


    def desyllabify(self, request: SyllableRequest) -> Response:
        """
        Given a word and its syllabified pronunciation (a SyllableRequest object),
        translate the Pronunciation object back to a string pronunciation for export
        in the format specified by the Config object.
        """
        pronunciation = self.syllable_builder.to_phonemes(request.pronunciation)
        return Response(request.word, pronunciation)


class CorpusFactory:
    def __init__(self, config: Config):
        self.config = config

    def create(self) -> Corpus:
        # TODO: map syllableBuilder to config, use this to get the correct
        # syllableBuilder in the corpus initialization
        pass



