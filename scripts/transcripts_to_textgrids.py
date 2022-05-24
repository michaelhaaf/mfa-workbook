#! /usr/bin/python3
# Adapted from:
# https://nbviewer.org/github/timmahrt/praatIO/blob/main/tutorials/tutorial1_intro_to_praatio.ipynb

import os
import re
import argparse

from praatio import textgrid
from praatio.utilities.constants import Interval

from functools import reduce


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def process_timestamp(line):
    return re.sub('[\[\]]', '', line)


# {LG} spn  unknown word
# {SL} sil  silence

# TODO: are these the only extra artifacts to remove?
def process_text(line):
    find_replace_chain = \
        ('<hes>', '{hes}'), \
        ('<breath>', '{LG}'), \
        ('<no-speech>', '{SL}'), \
        ('<sta>', '{LG}'), \
        ('<cough>', '{LG}'), \
        ('<lipsmack>', '{LG}'), \
        ('<int>', '{LG}'), \
        ('<click>', '{LG}'), \
        ('<prompt>', '{LG}'), \
        ('<female-to-male>', '{LG}'), \
        ('<male-to-female>', '{LG}'), \
        ('<cough>', '{LG}'), \
        ('<dtmf>', '{LG}'), \
        ('<foreign>', '{LG}'), \
        ('<overlap>', '{LG}'), \
        ('<ring>', '{LG}'), \
        ('\(\(\)\)', '{SL}'), \
        ('<[^>]*>', '{LG}'), \
        ('{hes}', '<hes>'), \
        ('[ ]{1,}', ' ')

    return reduce(lambda s, kv: re.sub(*kv, s), find_replace_chain, line).strip()


def process_intervals(filePath):
    intervals = []
    with open(filePath, "r") as f:
        loopLine = f.readline()
        while loopLine:
            startLine = process_timestamp(loopLine)
            textLine = process_text(f.readline())

            # each call to readline() advances the for loop.
            loopLine = f.readline()
            endLine = process_timestamp(loopLine)

            if textLine and endLine:
                intervals.append(Interval(startLine, endLine, textLine))
    return intervals


def main(args):

    inputPath = args.input
    outputPath = args.dest

    for fn in os.listdir(inputPath):
        name, ext = os.path.splitext(fn)
        if ext != ".txt":
            continue
        print(f"Processing {fn}...")

        intervals = process_intervals(os.path.join(inputPath, fn))
        duration = intervals[-1].end
        wordTier = textgrid.IntervalTier('words', intervals, 0, duration)

        tg = textgrid.Textgrid()
        tg.addTier(wordTier)
        tg.save(os.path.join(outputPath, name + ".TextGrid"),
                format="long_textgrid", includeBlankSpaces=True)

    # Did it work?
    for fn in os.listdir(outputPath):
        ext = os.path.splitext(fn)[1]
        if ext != ".TextGrid":
            continue
        print(fn)


# Usage
# python txt-to-textgrid.py --input input/ --dest dest/ 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='converts text transcript files to .TextGrids')
    parser.add_argument('--input',
                        required=True,
                        help='path to directory containing .txt transcripts',
                        type=dir_path,
                        dest='input'
                        )
    parser.add_argument('--dest',
                        required=True,
                        help='output dictionary path',
                        type=dir_path,
                        dest='dest'
                        )
    args = parser.parse_args()

    main(args)


