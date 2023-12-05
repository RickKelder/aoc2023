import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np

import time
start = time.time()

#file = getLinesAsOne("testinput.txt")
file = getLinesAsOne()

def getData(inputString):
    splitted = inputString.split("\n\n")
    return list(map(lambda data: data.split(":"), splitted))

def getDataFrames(dataArray):
    dataFrames = {}
    for data in dataArray:
        dataKey = "df_"+data[0].replace(" map","").replace("-","_")
        dataFrames[dataKey] = list(map(lambda splittedData: list(map(lambda intObj: int(intObj), splittedData.split(" "))), re.sub(r'^\s', '', data[1]).split("\n")))
        if dataKey == "df_seeds":
            dataFrames[dataKey] = pd.Series(dataFrames[dataKey][0])
            dataFrames[dataKey+"2"] = pd.Series([[dataFrames[dataKey][i],dataFrames[dataKey][i]+dataFrames[dataKey][i+1]] for i in range(0, len(dataFrames[dataKey]), 2)])
        else:
            dataFrames[dataKey] = pd.DataFrame(dataFrames[dataKey],  columns=['destination_from', 'source_from', 'range'])
            dataFrames[dataKey]['source_to'] = dataFrames[dataKey]['source_from']+dataFrames[dataKey]['range']
            dataFrames[dataKey]['diff'] = dataFrames[dataKey]['destination_from']-dataFrames[dataKey]['source_from']
    return dataFrames

dataFrames = getDataFrames(getData(file))
dataFramesDestinations = dict(filter(lambda dfItem: not dfItem[0].startswith("df_seeds"), dataFrames.items()))
seedFrame = dataFrames["df_seeds"].copy()

def getNewDestination(originalNumber, dataFrame):
    dfIsInRange = (dataFrame['source_from'] <= originalNumber) & (dataFrame['source_to'] > originalNumber)
    indexInRange = dfIsInRange[dfIsInRange].index #gets all trues as index
    return originalNumber if len(indexInRange) == 0 else originalNumber + dataFrame['diff'][indexInRange[0]]

def trackSeed(seedNumber, dataFramesInput):
    for dataFrameName in dataFramesInput:
        seedNumber = getNewDestination(seedNumber, dataFramesInput[dataFrameName])
    return seedNumber

seedFrame = seedFrame.apply(trackSeed, dataFramesInput=dataFramesDestinations)
print(seedFrame)
print(seedFrame.min())

seedFrame2 = dataFrames["df_seeds2"].copy()
print(seedFrame2)
print(dataFramesDestinations['df_seed_to_soil'])

def overlap(start1, end1, start2, end2):
    return (max(start1, start2), min(end1, end2)) if max(start1, start2) < min(end1, end2) else (0, 0)

def overlapDf(overlapDf, start1, end1):
    return overlap(start1, end1, overlapDf['source_from'], overlapDf['source_to'])

def splitByDestinationRange(inputFrame, dataFrameDestination):
    seedFrameChanged = pd.Series()
    for index, seedRange in inputFrame.items():
        dataFrame = dataFrameDestination
        dataFrameOverlap = dataFrame.apply(overlapDf, axis=1, start1=seedRange[0], end1=seedRange[1])
        newSeedRange = []
        overlapFromTo = [seedRange[0], seedRange[1]]
        for indexOverlap, seedRangeOverlap in dataFrameOverlap.items():
            if seedRangeOverlap != (0,0):
                overlapFromTo.append(seedRangeOverlap[0])
                overlapFromTo.append(seedRangeOverlap[1])
                overlapFromTo.sort()
                overlapFromTo = list( dict.fromkeys(overlapFromTo) )
        for index in range(len(overlapFromTo)-1):
            newSeedRange.append([overlapFromTo[index], overlapFromTo[index+1]])
        seedFrameChanged = seedFrameChanged.append(pd.Series(newSeedRange), ignore_index=True)
    return seedFrameChanged

def trackDestinationByRange(inputFrame, dataFrameDestination):
    seedFrameChanged = inputFrame.copy()
    for index, seedRange in inputFrame.items():
        dataFrame = dataFrameDestination
        dataFrameOverlap = dataFrame.apply(overlapDf, axis=1, start1=seedRange[0], end1=seedRange[1])
        for indexOverlap, seedRangeOverlap in dataFrameOverlap.items():
            if seedRangeOverlap != (0,0):
                seedFrameChanged[index] = [seedFrameChanged[index][0]+dataFrameDestination.loc[indexOverlap]['diff'], seedFrameChanged[index][1]+dataFrameDestination.loc[indexOverlap]['diff']]
    return seedFrameChanged
                
def trackSeedByRange(seedFrame, dataFramesInput):
    seedFrameReturn = seedFrame
    for dataFrameName in dataFramesInput:
        # probably could have gone into one function but I liked this more
        seedFrameReturn = splitByDestinationRange(seedFrameReturn, dataFramesInput[dataFrameName])
        seedFrameReturn = trackDestinationByRange(seedFrameReturn, dataFramesInput[dataFrameName])
    return seedFrameReturn

results = trackSeedByRange(seedFrame2, dataFramesInput=dataFramesDestinations)
print(results)
print(results.min())
print('It took', time.time()-start, 'seconds.')