import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np
import functools
import itertools
import operator
from functools import lru_cache

import time
start = time.time()

#lines = getLines("testinput.txt")
lines = getLines()

def getNewCharValue(oldValue, char):
    oldValue += ord(char)
    oldValue *= 17
    oldValue %= 256
    return oldValue

def getNewValue(stringValue):
    currentValue = 0
    for char in stringValue:
        currentValue = getNewCharValue(currentValue, char)
    return currentValue

steps = lines[0].split(",")
stepValues = []
for step in steps:
    stepValues.append(getNewValue(step))

print(sum(stepValues))

boxes = [{} for i in range(256)]
sequence = []
for step in steps:
    splitVal = step.split("-") if "-" in step else step.split("=")
    splitVal.append(getNewValue(splitVal[0]))
    sequence.append(splitVal)

for instruction in sequence:
    if instruction[1] == '':
        if instruction[0] in boxes[instruction[2]]:
            oldPos = boxes[instruction[2]][instruction[0]]["pos"]
            boxes[instruction[2]].pop(instruction[0], None)
            for key in boxes[instruction[2]]:
                if boxes[instruction[2]][key]["pos"] > oldPos:
                    boxes[instruction[2]][key]["pos"] -= 1
    else:
        boxes[instruction[2]][instruction[0]] = { "value": int(instruction[1]), "pos": len(boxes[instruction[2]]) if not instruction[0] in boxes[instruction[2]] else boxes[instruction[2]][instruction[0]]["pos"]}

print(boxes)
result = 0
for i in range(len(boxes)):
    for key in boxes[i]:
        result += (i+1)*(boxes[i][key]["pos"]+1)*(boxes[i][key]["value"])

print(result)

print('It took', time.time()-start, 'seconds.')
