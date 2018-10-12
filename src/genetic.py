# ch: Chromosome
#  n: size of population
#  l: size of chromosome
from random import choices, randint
from sys import exit
import random
import numpy

########################################################################
# Utility
########################################################################
def max_index(l):
    return max(enumerate(l), key = lambda x: x[1])

def min_index(l):
    return min(enumerate(l), key = lambda x: x[1])

########################################################################
# Domain specific functions
########################################################################
# Function for generating a forefather, a chromosome with no parent.
def forefather():
    return [randint(-10, 10) for _ in range(5)]

# To determine how close a chromosome comes to a polynomial.
def p(ch, x):
    #return ch[0]*x + ch[1]*x + ch[2]*x + ch[3]*x + ch[4]*x
    return ch[0]*x**4 + ch[1]*x**3 + ch[2]*x**2 + ch[3]*x + ch[4]

# Dummy fitness function. Calculates how well the chromosome
# approximates the poynomial 4x^4 - 2x^3 + 20x^2 + x - 40
def fitness(ch):
    w = [4, -2, 3, 1, -4]
    xs = [randint(-10, 10) for _ in range(10)]
    tss = sum((p(w, x) - p(ch, x))**2 for x in xs)
    return tss / len(xs)

########################################################################
# Genetic algorithm functions
########################################################################
# Computes fitness for each individual.
def population_fitness(pop, fit_fun):
    fits = [fit_fun(p) for p in pop]
    worst = max(fits)
    fits = [worst - fit for fit in fits]
    tot = sum(fits)
    return [f/tot for f in fits]
    # tot = sum(fits)
    # return list(reversed([f/tot for f in fits]))

def create_population(n, gen_fun, fit_fun):
    pop = [gen_fun() for _ in range(n)]
    return pop, population_fitness(pop, fit_fun)

def offsprint_of_two(individual1, individual2):
    where_to_split = random.randint(0, len(individual1))
    offsprings = []
    offsprings.append(individual1[:where_to_split] +
                      individual2[where_to_split:])
    offsprints.append(individual2[:where_to_split] +
                      individual1[where_to_split:])
    return offsprints

def mutate(ch):
    if randint(0, 100) == 100:
        idx = randint(0, len(ch) - 1)
        ch[idx] += randint(-1, 1)

# Perform mating of two chromosomes
def mate(pop, fits):
    while True:
        p1, p2 = choices(list(pop), list(fits), k = 2)
        if p1 != p2:
            break
    i = randint(0, len(p1))
    c1 = p1[:i] + p2[i:]
    c2 = p2[:i] + p1[i:]
    mutate(c1)
    mutate(c2)
    return [c1, c2]

def select(individuals, select_this_many):
    objective_values = [fitness(element) for element in individuals]
    probabilities = [objective_values[i]/sum(objective_values)
                     for i in range(len(objective_values))]
    chosen_indexes = list(numpy.random.choice(range(len(individuals)),
                                              select_this_many,
                                              False,
                                              probabilities))
    return [individuals[i] for i in chosen_indexes]

def optimize_it():
    # create 20 integer lists each having 5 elements and the elements
    # are from 1 to 10
    individuals = create_population(20, forefather)
    best_objective_value = 99999
    iteration = 0
    index_of_it = None
    while best_objective_value > 1000 and iteration < 100:
        individuals = select(individuals)
        # yet to be done
        individuals = create_offspring(individuals)
        # yet to be done
        individuals = mutate(individuals)

        #yet to be done
        best_objective_value, index_of_it = \
            compute_best_objective_value(individuals)
        iteration +=1

if __name__ == '__main__':
    pop, fits = create_population(50, forefather, fitness)
    for gen in range(1000):
        pop2 = []
        while len(pop2) < len(pop):
            pop2.extend(mate(pop, fits))
        pop = pop2
        fits = population_fitness(pop, fitness)
        i, v = max_index(fits)
        print(i, v, pop[i], fitness(pop[i]))
