import pandas as pd
import re


class PronunciationDict:
    file_keys = ["word", "pronunciation"]

    def __init__(self, tone_dict, col_name):
        self.tone_dict = tone_dict
        self.col_name = col_name

    def create_df_from_file(self, file_path):
        pass


class WikiPronPronunciationDict(PronunciationDict):
    def __init__(self):
        tone_dict = { # TODO: extract to config
            "˧": "33",     # mid
            "˨˩": "21",    # low
            "˩": "21",
            "˥˩": "43",    # falling
            "˦˥": "44",    # high
            "˥": "44",
            "˩˩˦": "323",   # rising
            "˩˦": "323"
        }
        col_name = "wp_tone"
        super().__init__(tone_dict, col_name)

    def create_df_from_file(self, file_path):
        frame = pd.read_csv(file_path,
                            delimiter="\t",
                            header=None,
                            names=super().file_keys,
                            index_col="word")
        return frame


class GlobalPhonePronunciationDict(PronunciationDict):
    def __init__(self):
        tone_dict = { # TODO: extact to config
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "0": "0"
        }
        col_name = "gp_tone"
        super().__init__(tone_dict, col_name)

    # Weird global phone processing magic
    def create_df_from_file(self, file_path):
        word_cleanup_pattern = re.compile(r'\(\d+\)')
        line_break_pattern = re.compile(r'\}\s+')
        word_pattern = re.compile(r'^{([^{}]+)\s+')

        data_dict = {}
        with open(file_path, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                try:
                    word, phones = line_break_pattern.split(line, maxsplit=1)
                except ValueError:
                    raise(
                        Exception('There was a problem with the line \'{}\'.'.format(line)))
                if 'SIL' in phones or '+QK' in phones:
                    continue
                word = word[1:].strip()
                if '{' in word:
                    word = word_pattern.match(line)
                    word = word.groups()[0]
                    phones = word_pattern.sub('', line)
                word = word_cleanup_pattern.sub('', word)
                word = word.strip()
                if word not in data_dict:
                    data_dict[word] = []

                # TODO: not this!!!
                phonemes = list(phones)
                phones = " ".join(phonemes)

                data_dict[word].append(phones)

        frame = [[key, value] for key, value in data_dict.items()]
        df = pd.DataFrame(frame, columns=super().file_keys)
        df.set_index("word", inplace=True)
        return df
