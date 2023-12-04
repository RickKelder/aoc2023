import sys
sys.path.append('../')
from helpers import getLines
import re
import pandas as pd
import numpy as np

#lines = getLines("testinput.txt")
lines = getLines()

def getScore(number):
    return pow(2, number-1) if number > 0 else 0

def getDataFrames(inputLines):
    winningList = [[] for i in range(len(inputLines))]
    owningList = [[] for i in range(len(inputLines))]
    for i in range(len(inputLines)):
        splittedLine = (inputLines[i].split(":")[1]).split("|")
        #too bad python cant do multiple group capturing with regex without an additional package :-(
        regexResultsWinning = re.findall("\s\d+", splittedLine[0])
        regexResultsOwning= re.findall("\s\d+", splittedLine[1])
        winningList[i] = map(lambda x: int(x), regexResultsWinning) 
        owningList[i] = map(lambda x: int(x), regexResultsOwning)
    return {
        "dfWinning": pd.DataFrame(winningList),
        "dfOwning": pd.DataFrame(owningList)
    }


dataFrames = getDataFrames(lines)
dfWinning = dataFrames["dfWinning"]
dfOwning = dataFrames["dfOwning"]
print("dfWinning:")
print(dfWinning)
print("dfOwning:")
print(dfOwning)

dfConcat = pd.concat([dfWinning, dfOwning], axis=1)
print("dfConcat:")
print(dfConcat)

dfDuplicates = dfConcat.apply(pd.Series.duplicated, axis=1)
print("dfDuplicates:")
print(dfDuplicates)

dfWinningOwning = dfConcat*dfDuplicates
print("dfWinningOwning:")
print(dfWinningOwning)

dfWinningOwningCount = dfWinningOwning.astype(bool).sum(axis=1)
print("dfWinningOwningCount:")
print(dfWinningOwningCount)

dfWinningOwningScore = dfWinningOwningCount.apply(getScore)
print("dfWinningOwningScore:")
print(dfWinningOwningScore)

print("solution 1:", dfWinningOwningScore.sum())

dfCards = pd.Series([1 for i in range(dfWinningOwningCount.shape[0])])
for i in range(dfWinningOwningCount.shape[0]):
    for j in range(i+1, min(dfWinningOwningCount.shape[0], i+1+dfWinningOwningCount[i])):
        dfCards[j] += dfCards[i]
print(dfCards)
print("solution 2:", dfCards.sum())