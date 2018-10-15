from src.environment import TetrisApp
import random

'''
Determines how good an AI player is by making it play several games
and counting the average number of rows it clears per game. This will be used
to compare different genetic algorithm (GA) solutions as well as GA's to
other local search algorithms
'''


def fitness(weights, sequence):
    App = TetrisApp(False, weights)
    return App.runSequenceNoGUI(sequence)


def fitnessAverage(weights, sequenceLength, iterations):
    scores = [0.0 for x in range(len(weights))]

    for iter in range(iterations):
        sequence = [random.randint(0, 6) for x in range(sequenceLength)]

        # Try every on of the weights
        for i in range(len(weights)):
            scores[i] += fitness(weights[i], sequence)

    return [score/iterations for score in scores]
