import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np
import functools 

import time
start = time.time()

lines = getLines("testinput.txt")
lines = getLines()

timeValues = list(map(lambda timeVal: int(timeVal), re.findall("\d+", lines[0].split(":")[1])))
distanceValues = list(map(lambda timeVal: int(timeVal), re.findall("\d+", lines[1].split(":")[1])))
print(timeValues, distanceValues)

def findMinimalDistance(maxTimeValue, distanceValue):
    for holdButtonMs in range(0, maxTimeValue):
        timeLeft = maxTimeValue - holdButtonMs
        if holdButtonMs * timeLeft > distanceValue:
            return holdButtonMs
        
def findMaximumDistance(maxTimeValue, distanceValue):
    for holdButtonMs in range(maxTimeValue, 0, -1):
        timeLeft = maxTimeValue - holdButtonMs
        if holdButtonMs * timeLeft > distanceValue:
            return holdButtonMs
        
def findNumRecord():
    numRecords = [0 for i in range(len(timeValues))]
    for i in range(len(timeValues)):
        numRecords[i] = findMaximumDistance(timeValues[i], distanceValues[i])-(findMinimalDistance(timeValues[i], distanceValues[i])-1)
    return numRecords

print("solution:", functools.reduce(lambda a,b: a*b, findNumRecord()))

timeValues = [int(functools.reduce(lambda a,b: str(a)+str(b), timeValues))]
distanceValues = [int(functools.reduce(lambda a,b: str(a)+str(b), distanceValues))]
print("solution:", functools.reduce(lambda a,b: a*b, findNumRecord()))

print('It took', time.time()-start, 'seconds.')