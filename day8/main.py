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

instruction = list(map(lambda char: 0 if char == "L" else 1, lines[0]))

routeDictionary = {route.split(" = ")[0]: list(map(lambda routeStr: routeStr.replace("(","").replace(")",""), route.split(" = ")[1].split(", "))) for route in lines[2:] }

todo = ['AAA']

currentInstruction = instruction
currentCost = 0
while True:
    if todo[0] == 'ZZZ':
        break
    currentCost += 1
    todo = list(map(lambda location: routeDictionary[location][currentInstruction[0]], todo))
    currentInstruction = instruction if len(currentInstruction[1:]) == 0 else currentInstruction[1:]

print(currentCost)

print('It took', time.time()-start, 'seconds.')