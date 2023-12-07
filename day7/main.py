import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np
import functools 

import time
start = time.time()

#lines = getLines("testinput.txt")
lines = getLines()

translateDictionary = {
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "T": "10",
    "J": "11",
    "Q": "12",
    "K": "13",
    "A": "14"
}

def parseLines(inputLines):
    games = [[] for i in range(len(inputLines))]
    for i in range(len(inputLines)):
        games[i] = list(map(lambda val: int(translateDictionary[val]), inputLines[i].split(" ")[0])) + [inputLines[i].split(" ")[0], int(inputLines[i].split(" ")[1])]
    return games

def calcHandStrength(row):
    filteredRow = row.drop(labels=['bid'])
    valueCounts = filteredRow.value_counts()
    strength = valueCounts.iloc[0]*10 + (0 if valueCounts.iloc[1] == 1 else valueCounts.iloc[1])
    return strength

def rowIndex(row, rowCount):
    return rowCount-row.name

dfGames = pd.DataFrame(parseLines(lines),  columns=['a', 'b', 'c', 'd', 'e', 'hand', 'bid'])
print(dfGames)
dfGames['strength'] = dfGames.apply(calcHandStrength, result_type="reduce", axis=1)
print(dfGames)
dfGamesSorted = dfGames.sort_values(['strength', 'a', 'b', 'c', 'd', 'e'], ascending=False)
dfGamesSorted.reset_index(inplace=True)
dfGamesSorted['rank'] = dfGamesSorted.apply(rowIndex, result_type="reduce", axis=1, rowCount=dfGamesSorted.shape[0])
dfGamesSorted['score'] = dfGamesSorted['rank'] * dfGamesSorted['bid']
pd.set_option('display.max_rows', dfGamesSorted.shape[0]+1)
print(dfGamesSorted)
print(dfGamesSorted['score'].sum())