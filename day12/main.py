import sys
sys.path.append('../')
from helpers import getLines, getLinesAsOne
import re
import pandas as pd
import numpy as np
import functools
from functools import lru_cache

import time
start = time.time()

lines = getLines("testinput.txt")
#lines = getLines()

@lru_cache()
def getCombinations(springLine, groupsToDo):
    if len(springLine) == 0:
        return 1 if len(groupsToDo) == 0 else 0
    if springLine[0] == ".":
        return getCombinations(springLine[1:], groupsToDo)
    if springLine[0] == "?":
        return getCombinations("."+springLine[1:], groupsToDo)+getCombinations("#"+springLine[1:], groupsToDo)
    if springLine[0] == "#":
        if len(groupsToDo) == 0 or len(springLine) < groupsToDo[0]:
            return 0
        if "." in springLine[:groupsToDo[0]]:
            return 0
        if len(springLine) > groupsToDo[0] and springLine[groupsToDo[0]] == "#":
            return 0
        return getCombinations("."+springLine[groupsToDo[0]+1:], groupsToDo[1:])
        
        
springs = list(map(lambda line: [line.split(" ")[0], tuple(list(map(lambda x: int(x), line.split(" ")[1].split(","))))], lines))
resultList = list(map(lambda springEntry: getCombinations(springEntry[0], springEntry[1]), springs))
print(resultList, sum(resultList))

springsUnfolded = list(map(lambda spring: [spring[0]+"?"+spring[0]+"?"+spring[0]+"?"+spring[0]+"?"+spring[0], spring[1]+spring[1]+spring[1]+spring[1]+spring[1]], springs))
resultListUnfolded = list(map(lambda springEntry: getCombinations(springEntry[0], springEntry[1]), springsUnfolded))
print(resultListUnfolded, sum(resultListUnfolded))

print('It took', time.time()-start, 'seconds.')