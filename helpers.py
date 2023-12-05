from typing import List

def getLines(filename="input.txt")-> List[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file]
    
def getLinesAsOne(filename="input.txt")-> List[str]:
    with open(filename) as file:
         return file.read()