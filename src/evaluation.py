from random import randint
from src.environment import TetrisApp
import random

"""
Determines how good an AI player is by making it play several games
and counting the average number of rows it clears per game. This will be used
to compare different genetic algorithm (GA) solutions as well as GA's to
other local search algorithms
"""


'''
Calculates fitness on a random sequence
'''
def fitnessRandom(weights):
    limit = 1000
    seq = [randint(0, 6) for _ in range(limit)]
    return TetrisApp(False, weights).runSequenceNoGUI(seq)


'''
Calculates fitness on a given sequence
'''
def fitness(weights, sequence):
     return TetrisApp(False, weights).runSequenceNoGUI(sequence)


'''
Generates several sequences and for every element in weight_list,
computes the average fitness
'''
def fitnessAverage(weight_list, sequenceLength, iterations):
    scores = [0.0 for x in range(len(weight_list))]

    for iteration in range(iterations):
        sequence = [random.randint(0, 6) for x in range(sequenceLength)]

        # Try every one of the weights
        for i in range(len(weight_list)):
            scores[i] += fitness(weight_list[i], sequence)

    return [score/iterations for score in scores]

