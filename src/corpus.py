from src.config import Config
from src.io import Request, SyllableRequest, Response
from src.syllableBuilder import SyllableBuilder


class Corpus:

    def __init__(self, config: Config, syllable_builder: SyllableBuilder):
        self.config = config
        self.fileio = fileio
        self.syllable_builder = syllable_builder


    def syllabify(self, request: Request) -> SyllableRequest:
        """
        Given a word and its phoneme set (a Request object),
        return the word and its pronunciation (a SyllableRequest
        object) transformed to an output format specified by the Config object.
        """
        syllables = [syllable_builder.from_phonemes(request.phonemes)]
        pronunciation = Pronunciation(syllables)
        return SyllableRequest(request.word, pronunciation)


    def desyllabify(self, request: SyllableRequest) -> Response:
        """
        Given a word and its syllabified pronunciation (a SyllableRequest object),
        dump the word and its pronunciation to FileIO for export in the format 
        specified by the Config object.
        """
        pronunciation = ""
        for syllable in request.pronunciation:
            nucleus = syllable.nucleus
            nucleus[0] = f"{nucleus[0] + syllable.tone}"
            pronunciation += config.phoneme_bound.join(syllable.onset) + config.phoneme_bound
            pronunciation += config.phoneme_bound.join(nucleus) + config.phoneme_bound
            pronunciation += config.phoneme_bound.join(syllable.coda)
            pronunciation += config.syllable_bound

        return Response(request.word, pronunciation)

class CorpusFactory:
    def create(self, config: Config) -> Corpus:



