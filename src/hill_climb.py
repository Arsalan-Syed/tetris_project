import numpy as np
import environment as env
import itertools
import copy

from src import filehandler

"""
This class is used to take some existing weights and optimize them using
a hill climbing algorithm. It takes the existing weights, find all possible 
neighbours by making small increments to the weights and then evaluates them
with the fitness function.  
"""

'''
Determines how good an AI player is by making it play several games
and counting the average number of rows it clears per game. This will be used
to compare different genetic algorithm (GA) solutions as well as GA's to
other local search algorithms
'''


# TODO use weights
def fitness(weights):
    filename = "../sequences/test1.txt"
    score = 0

    sequences = filehandler.loadSequences(filename)
    for sequence in sequences:
        App = env.TetrisApp(False)
        score += App.runSequenceNoGUI(filename, sequence)

    return score / len(sequences)


def convert(x):
    result = int(x)
    if result == 2:
        return -1
    return result


def getWeightVectorNeighbours(weights, stepSize):
    weightIncrements = []
    chars = "012"
    count = len(weights)
    for item in itertools.product(chars, repeat=count):
        weightIncrements.append([convert(x) for x in item])

    neighbours = []
    for increment in weightIncrements:
        delta = np.multiply(increment, stepSize)
        neighbours.append(np.add(weights, delta))
    return neighbours


def hill_climb(weight_vector):
    stepSize = 0.1
    current_weights = copy.deepcopy(weight_vector)

    while True:
        bestFitness = -10000000
        bestWeights = None
        for neighbour in getWeightVectorNeighbours(current_weights, stepSize):
            neighbourFitness = fitness(current_weights)
            if neighbourFitness > bestFitness:
                bestFitness = neighbourFitness
                bestWeights = neighbour

        if bestFitness <= fitness(current_weights):
            return current_weights

        current_weights = bestWeights
