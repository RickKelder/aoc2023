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
#lines = getLines("testinput2.txt")
#lines = getLines("testinput3.txt")
#lines = getLines("testinput4.txt")
#lines = getLines("testinput5.txt")
lines = getLines()

def findS():
    for i in range(len(lines)):
        if lines[i].find('S') != -1:
            return [i, lines[i].find('S')]
        
locationS = findS()

visited = []
visited.append(locationS)
currentDirection = [0, 1]
directionHistory = []
directionHistory.append(currentDirection)
currentLocation = locationS

def getNewDirection(direction, char):
    if (char == "7"):
        return [1, 0] if direction[1] == 1 else [0, -1]
    if (char == "J"):
        return [-1, 0] if direction[1] == 1 else [0, -1]
    if (char == "F"):
        return [1, 0] if direction[1] == -1 else [0, 1]
    if (char == "L"):
        return [-1, 0] if direction[1] == -1 else [0, 1]
    return direction

for i in range(200000):
    currentLocation = [currentLocation[0]+currentDirection[0], currentLocation[1]+currentDirection[1]]
    if currentLocation == locationS:
        break
    visited.append(currentLocation)
    directionHistory.append(currentDirection)
    currentDirection = getNewDirection(currentDirection, lines[currentLocation[0]][currentLocation[1]])

print(len(visited), len(visited)/2)

enclosed = []
for i in range(len(lines)):
    inOutCross = 0
    currentCross = ""
    for j in range(len(lines[0])):
        if [i, j] not in visited:
            if inOutCross % 2 == 1:
                enclosed.append([i,j])
        else:
            char = lines[i][j]
            if (char == "|"):
                inOutCross += 1
                currentCross = ""
            elif char == "L" or char == "7" or char == "F" or char == "J":
                currentCross = currentCross + char
            if len(currentCross) > 1:
                if currentCross == "L7":
                    inOutCross += 1
                if currentCross == "FJ":
                    inOutCross += 1
                currentCross = ""

print(enclosed, len(enclosed))

print('It took', time.time()-start, 'seconds.')