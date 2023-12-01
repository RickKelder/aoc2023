import sys
sys.path.append('../')
from helpers import getLines
import re


def getCalibration(line:str):
    return 0 if len(line)==0 else int(line[0:1]+line[-1:])

def filterCharacters(line:str):
    return re.sub('\D', '', line)

def filterSpelled(line:str):
    wordMap = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9" } 
    for word, replacement in wordMap.items():
        line = line.replace(word, word+replacement+word)
    return line

print(sum(map(getCalibration, map(filterCharacters, getLines()))))
print(sum(map(getCalibration, map(filterCharacters, map(filterSpelled, getLines())))))