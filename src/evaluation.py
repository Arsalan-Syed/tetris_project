from src import filehandler
from src.environment import TetrisApp
import numpy as np

'''
Determines how good an AI player is by making it play several games
and counting the average number of rows it clears per game. This will be used
to compare different genetic algorithm (GA) solutions as well as GA's to
other local search algorithms
'''


def fitness(weights):
    filename = "../sequences/test1.txt"
    score = 0

    sequences = filehandler.loadSequences(filename)
    for sequence in sequences:
        App = TetrisApp(False, weights)
        score += App.runSequenceNoGUI(sequence)
        print(score)

    return np.floor(score / len(sequences))


# Default, note 1000 total pieces used in test1.txt
print(fitness([1.0, 1.0, 5.0, 2.0, 1.0, 1.0, 1.0]))
