"""
Class responsible for I/O operations
"""

'''
Given a filename, will load it as a list of integers
'''


def loadSequences(filename):
    result = []

    f = open(filename, "r")
    text = f.read()

    splitByLine = text.split("\n")

    for line in splitByLine:
        textSplit = line.split(" ")[:-1]
        result.append([int(x) for x in textSplit])

    return result
