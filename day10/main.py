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
#lines = getLines()

print('It took', time.time()-start, 'seconds.')