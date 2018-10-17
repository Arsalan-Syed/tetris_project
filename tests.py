"""
Created by Björn Lindqvist on 12th October 2018

This file is intended for writing tests in.
"""
from src.evaluation import fitnessAverage
from src.hill_climb import hill_climb
from src.evaluation import fitness
from src.filehandler import loadSequences


def hill_climbing_optimization():
    iterations = 10
    sequence_length = 500
    sample_size = 100
    step_size = 0.25

    initial_weight_vector = [4.0, -2.0, -1.0, -1.0, -1.0]
    new_weight_vector = hill_climb(initial_weight_vector, step_size, sample_size, sequence_length)

    avg = fitnessAverage([initial_weight_vector,new_weight_vector], sequence_length, iterations)

    old_weights_average_score = avg[0]
    new_weights_average_score = avg[1]

    assert new_weights_average_score > old_weights_average_score


def compare_weights():
    iterations = 10
    sequence_length = 1000

    best_weights = [
        [4.0, -2.0, -1.0, -1.0, -1.0],# default
        [5.0, -3.0, -1.0, -0.5, -0.5],
        [4.5, -2.5, -1.5, -0.5, -0.5],
        [4.5, -2.5, -1.5, -2.0, -1.0]
    ]

    sequences = loadSequences("sequences/test1.txt")

    fitAvg = fitnessAverage(best_weights, sequence_length, iterations)

    i=0
    for weights in best_weights:
        print("Weights: ",weights)
        print("Average: ",fitAvg[i])
        print("Fixed sequence of length: ",len(sequences[0])," - Fitness: ", fitness(weights, sequences[0]))
        print("Fixed sequence of length: ",len(sequences[1])," - Fitness: ", fitness(weights, sequences[1]))
        print(" ")
        i+=1



if __name__ == '__main__':
    hill_climbing_tests()
    #compare_hill_climbing_weights()
