import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np
import functools
import itertools
import operator

import time
start = time.time()

#lines = getLines("testinput.txt")
lines = getLines()

def printGrid():
    for i in range(len(lines)):
        printRow = ""
        for j in range(len(lines[0])):
            printRow += [item for item in rows[i] if item.columnIndex == j][0].obstacleType if [item for item in rows[i] if item.columnIndex == j] else "."
        print(printRow)

class Obstacle():
    def __init__(self, rowIndex, columnIndex, obstacleType):
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex
        self.obstacleType = obstacleType

    def score(self, maxRows):
        return maxRows-self.rowIndex if self.obstacleType == "O" else 0
    
    def __repr__(self):
     return f"{self.obstacleType}({self.rowIndex},{self.columnIndex})"

rows = [[] for i in range(len(lines))]
columns = [[] for j in range(len(lines[0]))]

for i in range(len(lines)):
    for j in range(len(lines[0])):
        if lines[i][j] != ".":
            obstacle = Obstacle(i, j, lines[i][j])
            rows[i].append(obstacle)
            columns[j].append(obstacle)

def moveNorth():
    for column in columns:
        lastBlockade = -1 
        for obstacle in column:
            if obstacle.obstacleType == "O":
                rows[obstacle.rowIndex] = [item for item in rows[obstacle.rowIndex] if item != obstacle]
                obstacle.rowIndex = lastBlockade+1
                rows[obstacle.rowIndex].append(obstacle)
                rows[obstacle.rowIndex].sort(key=operator.attrgetter('columnIndex'))
            lastBlockade = obstacle.rowIndex

moveNorth()

def getScore():
    returnScore = 0
    for row in rows:
        for obstacle in row:
            returnScore += obstacle.score(len(lines))
    return returnScore

print(getScore())

def moveWest():
    for row in rows:
        lastBlockade = -1 
        for obstacle in row:
            if obstacle.obstacleType == "O":
                columns[obstacle.columnIndex] = [item for item in columns[obstacle.columnIndex] if item != obstacle]
                obstacle.columnIndex = lastBlockade+1
                columns[obstacle.columnIndex].append(obstacle)
                columns[obstacle.columnIndex].sort(key=operator.attrgetter('rowIndex'))
            lastBlockade = obstacle.columnIndex

def moveSouth():
    for column in columns:
        lastBlockade = len(lines)
        for i in range(len(column), 0, -1):
            obstacle = column[i-1]
            if obstacle.obstacleType == "O":
                rows[obstacle.rowIndex] = [item for item in rows[obstacle.rowIndex] if item != obstacle]
                obstacle.rowIndex = lastBlockade-1
                rows[obstacle.rowIndex].append(obstacle)
                rows[obstacle.rowIndex].sort(key=operator.attrgetter('columnIndex'))
            lastBlockade = obstacle.rowIndex

def moveEast():
    for row in rows:
        lastBlockade = len(lines[0])
        for i in range(len(row), 0, -1):
            obstacle = row[i-1]
            if obstacle.obstacleType == "O":
                columns[obstacle.columnIndex] = [item for item in columns[obstacle.columnIndex] if item != obstacle]
                obstacle.columnIndex = lastBlockade-1
                columns[obstacle.columnIndex].append(obstacle)
                columns[obstacle.columnIndex].sort(key=operator.attrgetter('rowIndex'))
            lastBlockade = obstacle.columnIndex

moveWest()
moveSouth()
moveEast()

def doCycle():
    moveNorth()
    moveWest()
    moveSouth()
    moveEast()

# warmup
for i in range(499):
    doCycle()
    
# try to find pattern
pattern = []
for i in range(3000):
    doCycle()
    if len(pattern) % 2 == 0 and len(pattern) > 4:
        if pattern[:int(len(pattern)/2)] == pattern[int(len(pattern)/2):]:
            break
    pattern.append(getScore())
    if i%500==0:
        print(i)
print(len(pattern), pattern)

# do leftover cycles
amountOfCyclesLeft = 1000000000-501-i
amountOfCyclesLeftModulo = amountOfCyclesLeft%int(len(pattern)/2)
for i in range(amountOfCyclesLeftModulo):
    doCycle()

print(getScore())

print('It took', time.time()-start, 'seconds.')
