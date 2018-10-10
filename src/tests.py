import numpy as np


def generatePieces(length):
    return np.random.randint(7, size=length)


def writeToFile(filename, text):
    f = open(filename, "a")
    f.write(str(text))


'''
When comparing algorithms, they need to be tested on the exact same
sequence
'''


def savePieces():
    pieces = generatePieces(100)
    writeToFile("test1.txt", pieces)
