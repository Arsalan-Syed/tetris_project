# ch: Chromosome
#  n: size of population
#  l: size of chromosome
from bisect import bisect
from itertools import accumulate
from random import randint, random, randrange
from statistics import mean, stdev
from sys import exit
import numpy

def choices(population, weights=None, *, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.
    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    n = len(population)
    if cum_weights is None:
        if weights is None:
            _int = int
            return [population[_int(random() * n)] for i in range(k)]
        cum_weights = list(accumulate(weights))
    elif weights is not None:
        raise TypeError('Cannot specify both weights and cumulative weights')
    if len(cum_weights) != n:
        raise ValueError('The number of weights does not match the population')
    total = cum_weights[-1]
    hi = n - 1
    return [population[bisect(cum_weights, random() * total, 0, hi)]
            for i in range(k)]

########################################################################
# Utility
########################################################################
def max_index(l):
    return max(enumerate(l), key = lambda x: x[1])

def min_index(l):
    return min(enumerate(l), key = lambda x: x[1])

########################################################################
# Domain specific functions and classes
########################################################################
# Function for generating a forefather, a chromosome with no parent.
def forefather():
    v = 10
    return tuple([randint(-v, v) for _ in range(5)])

# To determine how close a chromosome comes to a polynomial.
def p(ch, x):
    #return ch[0]*x + ch[1]*x + ch[2]*x + ch[3]*x + ch[4]*x
    return ch[0]*x**4 + ch[1]*x**3 + ch[2]*x**2 + ch[3]*x + ch[4]

# Dummy fitness function. Calculates how well the chromosome
# approximates the poynomial 4x^4 - 2x^3 + 3x^2 + x - 4
def fitness(ch):
    w = (4, -2, 3, 1, -4)
    xs = [randint(-100, 100) for _ in range(10)]
    xs = [abs(p(w, x) - p(ch, x))**4 for x in xs]
    return mean(xs)

########################################################################
# Genetic algorithm functions
########################################################################
def population_fitness(pop, fit_fun):
    '''Computes fitness for each individual.'''
    fits = [fit_fun(p) for p in pop]
    worst = max(fits)
    fits = [worst - fit for fit in fits]
    tot = sum(fits)
    return [f / tot for f in fits]

def create_population(n, gen_fun, fit_fun):
    for _ in range(n):
        ch = gen_fun()
        yield fit_fun(ch), ch

def mutate(ch):
    if randint(0, 100) == 100:
        ch = list(ch)
        ch[randrange(0, len(ch))] += randint(-2, 2)
        ch = tuple(ch)
    return ch

# Two chromosomes get down and dirty
def mate(parent1, parent2):
    i = randint(0, len(parent1))
    code1, code2 = parent1[1], parent2[1]
    child_code1 = mutate(code1[:i] + code2[i:])
    child_code2 = mutate(code2[:i] + code1[i:])
    return child_code1, child_code2

def breed_population(pop, fit_fun):
    # We take the raw fitness values and converts them to
    # probabilities.
    fits = [p[0] for p in pop]
    worst = max(fits)
    fits = [worst - fit for fit in fits]
    tot = sum(fits)
    probs = [fit / tot for fit in fits]
    pop2 = []

    while len(pop2) < len(pop):
        # Find two individuals, based on their fitness probability
        while True:
            p1, p2 = choices(pop, probs, k = 2)
            if p1 != p2:
                break
        c1, c2 = mate(p1, p2)
        # Calculate their fitness and insert them in the new
        # population.
        pop2.append((fit_fun(c1), c1))
        pop2.append((fit_fun(c2), c2))
        # Also insert their parents
        pop2.append(p1)
        pop2.append(p2)
    return pop2

# Prints some data about the generation.
def generation_stats(pop):
    i, v = min_index(pop)
    fits = [p[0] for p in pop]
    fmt = '{:>10.3e} {:>10.3e} {:>10.3e} {:>10.3e} {!s:<23}'
    print(fmt.format(min(fits), mean(fits), max(fits), stdev(fits), v[1]))

if __name__ == '__main__':
    pop = list(create_population(5000, forefather, fitness))
    for gen in range(1000):
        pop = breed_population(pop, fitness)
        if gen % 500:
            generation_stats(pop)
