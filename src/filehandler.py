import numpy as np


def generatePieces(length):
    return np.random.randint(7, size=length)


def writeToFile(filename, array):
    f = open(filename, "a")
    for element in array:
        f.write(str(element)+" ")
    f.write("\n")


'''
When comparing algorithms, they need to be tested on the exact same
sequence
'''


def saveSequences(numberOfLines, sequenceLength):
    for i in range(numberOfLines):
        pieces = generatePieces(sequenceLength)
        writeToFile("../sequences/test1.txt", pieces)


def loadSequences(filename):
    result = []

    f = open(filename, "r")
    text = f.read()

    splitByLine = text.split("\n")

    for line in splitByLine:
        textSplit = line.split(" ")[:-1]
        result.append([int(x) for x in textSplit])

    return result

