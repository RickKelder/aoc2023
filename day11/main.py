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

galaxies = []
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] != '.':
            galaxies.append([i, j])

dfGalaxies = pd.DataFrame(galaxies, columns=['x', 'y'])

emptyX = pd.Series(range(len(lines)))[~pd.Series(range(len(lines))).isin(dfGalaxies['x'])]
emptyY = pd.Series(range(len(lines)))[~pd.Series(range(len(lines))).isin(dfGalaxies['y'])]

def getManhattanDistanceForGalaxies(dfGalaxyFrame, galaxyLengthTimesLarger=2):
    dfGalaxyFrame = dfGalaxyFrame.copy()
    xAddition = dfGalaxyFrame['x'] * 0
    for i in emptyX:
        for j in xAddition.index:
            if dfGalaxyFrame['x'][j] > emptyX[i]:
                xAddition[j] += galaxyLengthTimesLarger-1

    dfGalaxyFrame['x'] = dfGalaxyFrame['x']+xAddition

    yAddition = dfGalaxies['y'] * 0
    for i in emptyY:
        for j in yAddition.index:
            if dfGalaxies['y'][j] > emptyY[i]:
                yAddition[j] += galaxyLengthTimesLarger-1

    dfGalaxyFrame['y'] = dfGalaxyFrame['y']+yAddition

    manhattanDistances = []
    for i in range(dfGalaxyFrame.shape[0]):
        for j in range(i+1, dfGalaxyFrame.shape[0]):
            manhattanDistances.append(abs(dfGalaxyFrame.iloc[i]['x']-dfGalaxyFrame.iloc[j]['x']) + abs(dfGalaxyFrame.iloc[i]['y']-dfGalaxyFrame.iloc[j]['y']))
    return manhattanDistances

print("part1:", sum(getManhattanDistanceForGalaxies(dfGalaxies)))
print("part2:", sum(getManhattanDistanceForGalaxies(dfGalaxies, 1000000)))

print('It took', time.time()-start, 'seconds.')