# Modified from:
# https://nbviewer.org/github/timmahrt/praatIO/blob/main/tutorials/tutorial1_intro_to_praatio.ipynb

import os
import re

from praatio import textgrid
from praatio.utilities.constants import Interval

from functools import reduce


def process_timestamp(line):
    return re.sub('[\[\]]', '', line)


def process_text(line):
    find_replace_chain = ('\<.*\>', ''), ('\(\(\)\)', ''), ('[ ]{1,}', ' ')
    return reduce(lambda s, kv: re.sub(*kv, s), find_replace_chain, line)


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


### TODO: give running instructions or allow parameters
inputPath = os.path.join('data', 'transcript_roman')
outputPath = os.path.join(inputPath, "generated_textgrids")

if not os.path.exists(outputPath):
    os.mkdir(outputPath)

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
    tg.save(os.path.join(outputPath, name + ".TextGrid"), format="long_textgrid", includeBlankSpaces=True)

# Did it work?
for fn in os.listdir(outputPath):
    ext = os.path.splitext(fn)[1]
    if ext != ".TextGrid":
        continue
    print(fn)
