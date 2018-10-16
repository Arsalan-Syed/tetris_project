# ch: Chromosome
#  n: size of population
#  l: size of chromosome
from bisect import bisect
from itertools import accumulate
from random import randint, random, randrange, uniform
from statistics import mean, stdev

"""
Represents the genetic algorithm
"""

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
# Genetic algorithm functions
########################################################################
def population_fitness(pop, fit_fun):
    # Computes fitness for each individual.
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
    mutate_range = 10
    perturb_range = 0.5
    for i in range(len(ch)):
        # 2% of a major mutation, otherwise perturb the gene just a
        # little.
        if randrange(50) == 0:
            v = mutate_range
        else:
            v = perturb_range
        ch[i] += -v + 2 * random() * v
    return ch

def mate2(parent1, parent2):
    number_of_genes_from_second_parent = randint(1,len(parent2))
    child1 = parent1[:]
    child2 = parent2[:]
    for i in random.sample(range(5), k=number_of_genes_from_second_parent):
        child1[i] = parent2[i]
    for i in random.sample(range(5), k=number_of_genes_from_second_parent):
        child2[i] = parent1[i]
    return child1, child2
# Two chromosomes get down and dirty
def mate(parent1, parent2):
    i = randint(0, len(parent1))
    code1, code2 = parent1[1], parent2[1]
    child_code1 = mutate(code1[:i] + code2[i:])
    child_code2 = mutate(code2[:i] + code1[i:])
    return child_code1, child_code2

def breed_population(pop, fit_fun, higher_better):
    n = len(pop)
    # Many possibilities here. Elitist selection: take the 10% best
    # and only breed on them:
    pop = sorted(pop)
    if higher_better:
        pop = list(reversed(pop))
    pop = pop[:len(pop)//10]
    # Roulette wheel section based on probabilities. Doesn't seem to
    # converge as quickly.
    # fits = [p[0] for p in pop]
    # worst = max(fits)
    # fits = [worst - fit for fit in fits]
    # tot = sum(fits)
    # probs = [fit / tot for fit in fits]
    pop2 = []

    while len(pop2) < n:
        # Perhaps we can allow mating with itself because it is
        # unlikely.
        p1, p2 = choices(pop, k = 2)
        # Find two individuals, based on their fitness probability
        # for _ in range(20):
        #     p1, p2 = choices(pop, k = 2) # , probs, k = 2)
        #     if p1 != p2:
        #         break
        c1, c2 = mate(p1, p2)
        # Calculate their fitness and insert them in the new
        # population.
        pop2.append((fit_fun(c1), c1))
        pop2.append((fit_fun(c2), c2))
        # Also insert their parents
        # pop2.append((fit_fun(p1[1]), p1[1]))
        # pop2.append((fit_fun(p2[1]), p2[1]))
    return pop2

# Prints some data about the generation.
def generation_stats(gen, pop, higher_better):
    if higher_better:
        best_score, best_gene = max(pop)
    else:
        best_score, best_gene = min(pop)
    fits = [p[0] for p in pop]
    fmt = '{:>3} {:>10.3e}, {:>10.3e}, {:>10.3e} {:>10.3e} [{}]'
    items = ' '.join('{:>7.3f}'.format(e) for e in best_gene)
    print(fmt.format(gen, min(fits), mean(fits), max(fits), stdev(fits), items))
    print('[%.3f, %.3f, %.3f],' % (min(fits), mean(fits), max(fits)))

def run_evolution(forefather, fitness, n, n_gens, higher_better):
    fmt = '* Running evolution for {0} generations with population size' \
        ' {1}, {2} scores better.'
    s = 'higher' if higher_better else 'lower'
    print(fmt.format(n_gens, n, s))
    pop = list(create_population(n, forefather, fitness))
    for gen in range(n_gens):
        generation_stats(gen, pop, higher_better)
        pop = breed_population(pop, fitness, higher_better)

def evolve_tetris():
    from evaluation import fitnessRandom
    def forefather():
        return [uniform(-10, 10) for _ in range(5)]
    run_evolution(forefather, fitnessRandom, 100, 50, True)

# def evolve_polynomial():
#     # Function for generating a forefather, a chromosome with no parent.
#     def forefather():
#         v = 1000
#         return [randint(-v, v) for _ in range(5)]

#     # To determine how close a chromosome comes to a polynomial.
#     def p(ch, x):
#         #return ch[0]*x + ch[1]*x + ch[2]*x + ch[3]*x + ch[4]*x
#         return ch[0]*x**4 + ch[1]*x**3 + ch[2]*x**2 + ch[3]*x + ch[4]

#     # Dummy fitness function. Calculates how well the chromosome
#     # approximates the polynomial 4x^4 - 2x^3 + 3x^2 + x - 4
#     def fitness(ch):
#         w = (4, -2, 3, 1, -4)
#         xs = [randint(-100, 100) for _ in range(100)]
#         xs = [abs(p(w, x) - p(ch, x))**2 for x in xs]
#         return mean(xs)
#     run_evolution(forefather, fitness, 100, False)

if __name__ == '__main__':
    #evolve_polynomial()
    evolve_tetris()
