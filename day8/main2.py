import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np
import functools 
import math

import time
start = time.time()

#lines = getLines("testinput2.txt")
lines = getLines()

instruction = list(map(lambda char: 0 if char == "L" else 1, lines[0]))

routeDictionary = {route.split(" = ")[0]: list(map(lambda routeStr: routeStr.replace("(","").replace(")",""), route.split(" = ")[1].split(", "))) for route in lines[2:] }

todo = []
for route in routeDictionary:
    if route.endswith("A"):
        todo.append(route)
checkString = "".join(["Z" for i in range(len(todo))])

currentInstruction = instruction
currentCost = 0

costsDone = []
while True:
    for appendVal in [val for val in todo if val.endswith("Z")]:
        costsDone.append(currentCost)
    todo = [val for val in todo if not val.endswith("Z")]
    if len(todo) == 0:
        break
    currentCost += 1
    todo = list(map(lambda location: routeDictionary[location][currentInstruction[0]], todo))
    currentInstruction = instruction if len(currentInstruction[1:]) == 0 else currentInstruction[1:]

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

print(functools.reduce(lambda a,b: lcm(a, b), costsDone))

print('It took', time.time()-start, 'seconds.')