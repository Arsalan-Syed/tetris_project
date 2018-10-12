import itertools
from src.helper import *
from src.evaluation import *
import random

"""
This class is used to take some existing weights and optimize them using
a hill climbing algorithm. It takes the existing weights, find all possible 
neighbours by making small increments to the weights and then evaluates them
with the fitness function.  
"""

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

    sampleSize = 10
    return random.sample(neighbours, sampleSize)


def hill_climb(weight_vector):
    stepSize = 0.1
    current_weights = copy.deepcopy(weight_vector)

    while True:
        bestFitness = -10000000
        bestWeights = None
        print(current_weights)
        for neighbour in getWeightVectorNeighbours(current_weights, stepSize):
            neighbourFitness = fitness(neighbour)
            if neighbourFitness > bestFitness:
                bestFitness = neighbourFitness
                bestWeights = neighbour

        if bestFitness <= fitness(current_weights):
            return current_weights

        current_weights = bestWeights

hill_climb([1.0, 1.0, 5.0, 2.0, 1.0, 1.0, 1.0, 1.0])
