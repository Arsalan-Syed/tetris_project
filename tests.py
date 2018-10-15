"""
Created by Björn Lindqvist on 12th October 2018

This file is intended for writing tests in.
"""
from src.evaluation import fitnessAverage
from src.hill_climb import hill_climb
from src.evaluation import fitness
from src.filehandler import loadSequences


def hill_climbing_tests():
    iterations = 10
    sequence_length = 200
    sample_size = 50
    step_size = 0.5

    initial_weight_vector = [1.0, 4.0, -2.0, -1.0, -1.0, -1.0]
    new_weight_vector = hill_climb(initial_weight_vector, step_size, sample_size, sequence_length)

    avg = fitnessAverage([initial_weight_vector,new_weight_vector], sequence_length, iterations)

    old_weights_average_score = avg[0]
    new_weights_average_score = avg[1]

    assert new_weights_average_score > old_weights_average_score


def compare_hill_climbing_weights():
    iterations = 10
    sequence_length = 200

    best_weights = [
        [1.0, 4.0, -2.0, -1.0, -1.0, -1.0], # default
        [0.0, 4.5, -2.5, -1.5, -2.0, -1.0], #following 4 found by hill climb
        [1.0, 4.5, -2.5, -0.5, -0.5, -0.5],
        [0.0, 4.0, -2.5, -0.5, -1.0, 0.0],
        [0.5, 3.0, -2.0, -1.5, -1.0, 0.0]
    ]

    sequences = loadSequences("sequences/test1.txt")

    print("Average: ", fitnessAverage(best_weights, sequence_length, iterations))

    print(" ")

    for weights in best_weights:
        print("Weights: ",weights)
        print("Fixed sequence of length: ",len(sequences[0])," - Fitness: ", fitness(weights, sequences[0]))
        print("Fixed sequence of length: ",len(sequences[1])," - Fitness: ", fitness(weights, sequences[1]))
        print(" ")



if __name__ == '__main__':
    #hill_climbing_tests()
    compare_hill_climbing_weights()
