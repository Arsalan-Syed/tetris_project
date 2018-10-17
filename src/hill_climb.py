import itertools
from src.evaluation import *
import random

"""
This class is used to take some existing weights and optimize them using
a hill climbing algorithm. It takes the existing weights, find all possible 
neighbours by making small increments to the weights and then evaluates them
with the fitness function.  
"""

'''
Converts a character to an integer
'''
def convert(x):
    result = int(x)
    if result == 2:
        return -1
    return result

'''
Finds all possible weight vectors obtained by applying
a positive/negative difference to each coefficient.

0 represents no change
1 represents a positive change
2 represents a negative change

returns a sample of these possible weights
'''
def getWeightVectorNeighbours(weights, stepSize, sampleSize):
    weightIncrements = []
    chars = "012"
    count = len(weights)

    # Generate all possible coefficient differences
    for item in itertools.product(chars, repeat=count):
        weightIncrements.append([convert(x) for x in item])

    # Find all possible weights
    neighbours = []
    for increment in weightIncrements:
        delta = [x * stepSize for x in increment]
        neighbour = weights.copy()
        for i in range(len(delta)):
            neighbour[i] += delta[i]
            neighbours.append(neighbour)

    # Return a sample of these possible new weights
    if len(neighbours) > sampleSize:
        return random.sample(neighbours, sampleSize)
    else:
        return neighbours

'''
Performs a hill climbing search to improve upon 
some initial weights. 
'''
def hill_climb(weight_vector, stepSize, samepleSize, sequenceLength):
    # Specify the number of sequences here
    seqAmount = 5

    sequences = [[random.randint(0, 6) for x in range(sequenceLength)] for _ in range(seqAmount)]

    current_weights = weight_vector.copy()
    current_fitness = fitness(current_weights, sequences[0])
    for sequence in sequences[1:]:
        current_fitness = min(current_fitness, fitness(current_weights, sequence))

    while True:
        bestFitness = -10000000
        bestWeights = None

        print(current_weights, current_fitness)


        for neighbour in getWeightVectorNeighbours(current_weights, stepSize, samepleSize):
            # Set fitness to the worst possible out of all sequences
            neighbourFitness = fitness(neighbour, sequences[0])
            for sequence in sequences[1:]:
                neighbourFitness = min(neighbourFitness, fitness(neighbour, sequence))

            # Found an improvement
            if neighbourFitness > bestFitness:
                bestFitness = neighbourFitness
                bestWeights = neighbour

        # No more improvements found
        if bestFitness <= current_fitness:
            print("Best: ", current_weights, current_fitness)
            return current_weights

        current_weights = bestWeights
        current_fitness = bestFitness
