import random
from typing import List, Any, Union

import numpy


def obj_func(coded_string):
    return random.randint(1, 100)


def create_initial_population(size_of_initial_population, coded_string_length, range_of_genes_maximum):
    population = [(random.sample(range(1, range_of_genes_maximum), coded_string_length)) for _ in
                  range(size_of_initial_population)]
    # for i in range(len(population)):
    #    population[i].sort()
    return population


def obj_func(individual):
    return random.randint(1, 10)


def offspring_of_two(individual1, individual2):
    where_to_split = random.randint(0, len(individual1))
    offsprings = []
    offsprings.append(individual1[:where_to_split] + individual2[where_to_split:])
    offsprings.append(individual2[:where_to_split] + individual1[where_to_split:])
    return offsprings

def create_offspring(individuals, select_this_many):
    #Here we will create all the possible off springs for the individuals selected to procreate
    nextgen = []
    for i in range(select_this_many):
        for j in range(select_this_many):
            if(i!=j):
                nextgen.append(offspring_of_two(individuals[i], individuals[j]))

    return nextgen

def mutate(individuals, number_elements_to_mutate):
    length_of_individuals = len(individuals[0])
    individuals_for_mutation = random.sample(individuals, number_elements_to_mutate)

    for i in range(number_elements_to_mutate):
        for j in range(length_of_individuals) :
            individuals_for_mutation[i][j] = random.randint(1,10)

    return individuals_for_mutation

def select(individuals, select_this_many):
    objective_values = [obj_func(element) for element in individuals]
    probabilities = [objective_values[i] / sum(objective_values) for i in range(len(objective_values))]
    chosen_indexes = list(numpy.random.choice(range(len(individuals)), select_this_many, False, probabilities))
    return [individuals[i] for i in chosen_indexes]


def optimize_it():
    individuals = create_initial_population(20, 5, 10)  # create 20 integer lists each having 5 elements and the elements are from 1 to 10
    best_objective_value = 99999
    iteration = 0
    index_of_it = None
    select_this_many = 5
    while (best_objective_value > 1000 and iteration < 100):
        individuals = select(individuals, select_this_many)

        individuals = create_offspring(individuals, select_this_many) #yet to be done

        individuals = mutate(individuals) #yet to be done

        best_objective_value, index_of_it = compute_best_objective_value(individuals) #yet to be done

        iteration += 1
