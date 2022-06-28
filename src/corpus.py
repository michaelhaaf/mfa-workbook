from enum import Enum, auto
from src.model import Pronunciation
from src.config import Config
from src.io import Request, SyllableRequest, Response
from src.syllable_builders.syllable_builder import SyllableBuilderInterface, SyllableBuilder, SyllableBuilderException
from src.syllable_builders.iarpa_canto import IARPA_Canto_Builder
from src.syllable_builders.iarpa_lithu import IARPA_Lithu_Builder
from src.syllable_builders.iarpa_lao import IARPA_Lao_Builder
from src.syllable_builders.mfa import MFA_Builder


class CorpusEnum(Enum):
    MFA = auto()
    IARPA_CANTO = auto()
    IARPA_LITHU = auto()
    IARPA_LAO = auto()


class Corpus:

    def __init__(self, syllable_builder: SyllableBuilderInterface):
        self.syllable_builder = syllable_builder


    def syllabify(self, request: Request) -> SyllableRequest:
        """
        Given a word and its phoneme set (a Request object),
        return the word and its pronunciation (a SyllableRequest
        object) transformed to an output format specified by the Config object.
        """
        try:
            syllables = [self.syllable_builder.from_phonemes(p) for p in request.phonemes]
        except SyllableBuilderException as ex:
            print(f"Skipping entry: \n\t{request} \n\t{ex}")
            return None

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
        self.corpus_mapping = {
            CorpusEnum.MFA: MFA_Builder(config),
            CorpusEnum.IARPA_LITHU: IARPA_Lithu_Builder(config),
            CorpusEnum.IARPA_LAO: IARPA_Lao_Builder(config),
            CorpusEnum.IARPA_CANTO: IARPA_Canto_Builder(config)
            }


    def create(self, corpus: str) -> Corpus:
        return Corpus(self.corpus_mapping[CorpusEnum[corpus]])
