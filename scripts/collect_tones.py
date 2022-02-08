from src.dictionary import WikiPronPronunciationDict, GlobalPhonePronunciationDict
import os
import re
import sys
import argparse
import pandas as pd

from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))


source_dictionary_map = {
    "wikiPron": WikiPronPronunciationDict(),
    "globalPhone": GlobalPhonePronunciationDict()
}


def tone_lookup(word, df, tone_dict):
    try:
        pronunciation = str(df.loc[word].pronunciation)
    except KeyError:
        return ["N/A"]

    tones = [tone_dict.get(token) for token in pronunciation.split(" ")]
    return list(filter(None, tones))


def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid file")


def main(args):

    df = pd.read_csv(args.intrinsicf0_path, delimiter=",")
    pronunciation_dict = source_dictionary_map[args.source]

    df[pronunciation_dict.col_name] = df['word'].apply(tone_lookup,
                                                       df=pronunciation_dict.create_df_from_file(
                                                           args.pronunciation_dict_path),
                                                       tone_dict=pronunciation_dict.tone_dict)

    print(f"{args.source} tone information computed.")
    command = input(
        "Preview results, or overwrite {args.intrinsicf0_path}? [p/o]\r\n")
    if command.lower() != 'o':
        print("Preview:")
        print(df)
    else:
        print(f"Overwriting {args.intrinsicf0_path}...")
        df.to_csv(args.intrinsicf0_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='adds tone information to intrinsicf0 file')
    parser.add_argument('--pronunciation-dict',
                        required=True,
                        help='path to file containing pronunciation dictionary',
                        type=file_path,
                        dest='pronunciation_dict_path'
                        )
    parser.add_argument('--intrinsicf0',
                        required=True,
                        help='path to intrinsicf0 file',
                        type=file_path,
                        dest='intrinsicf0_path'
                        )
    parser.add_argument('--source',
                        required=True,
                        help='wikipron or globalphone?',
                        choices=source_dictionary_map.keys(),
                        dest='source'
                        )
    args = parser.parse_args()

    main(args)
