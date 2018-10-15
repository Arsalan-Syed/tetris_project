from math import floor
from src import filehandler
from src.environment import TetrisApp

'''
Determines how good an AI player is by making it play several games
and counting the average number of rows it clears per game. This will be used
to compare different genetic algorithm (GA) solutions as well as GA's to
other local search algorithms
'''


def fitness(weights):
    filename = "../sequences/test1.txt"
    score = 0
    limit = 1000 # TODO change if needed

    sequences = filehandler.loadSequences(filename)
    for sequence in sequences:
        App = TetrisApp(False, weights)
        score += App.runSequenceNoGUI(sequence[0:limit])

    return floor(score / len(sequences))
