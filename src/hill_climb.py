import itertools
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


def getWeightVectorNeighbours(weights, stepSize, sampleSize):
    weightIncrements = []
    chars = "012"
    count = len(weights)
    for item in itertools.product(chars, repeat=count):
        weightIncrements.append([convert(x) for x in item])

    neighbours = []
    for increment in weightIncrements:
        delta = [x * stepSize for x in increment]
        neighbour = weights.copy()
        for i in range(len(delta)):
            neighbour[i] += delta[i]
            neighbours.append(neighbour)

    if len(neighbours) > sampleSize:
        return random.sample(neighbours, sampleSize)
    else:
        return neighbours


def hill_climb(weight_vector, stepSize, samepleSize, sequenceLength):
    current_weights = weight_vector.copy()
    sequence = [random.randint(0, 6) for x in range(sequenceLength)]

    while True:
        bestFitness = -10000000
        bestWeights = None

        print(current_weights, fitness(current_weights, sequence))

        for neighbour in getWeightVectorNeighbours(current_weights, stepSize, samepleSize):
            neighbourFitness = fitness(neighbour, sequence)
            if neighbourFitness > bestFitness:
                bestFitness = neighbourFitness
                bestWeights = neighbour

        if bestFitness <= fitness(current_weights, sequence):
            print("Best: ", current_weights, fitness(current_weights, sequence))
            return current_weights

        current_weights = bestWeights
