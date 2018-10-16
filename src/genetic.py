from bisect import bisect
from itertools import accumulate
from random import randint, random, randrange, sample, uniform
from statistics import mean, stdev

########################################################################
# Execution Parameters
########################################################################

# Whether to print generation stats
DEBUG_OUTPUT = True

# Individuals in population
POP_SIZE = 100

# Number of generations
N_GENS = 50

# Probability 0-100% of a gene being mutated
P_MUTATION = 5

# Whether to use 'single' crossover (mate) or 'uniform' (mate2)
CROSSOVER_TYPE = 'single'

# Fraction of the population in elitist selection (0.1 = 10%)
ELITE_FRACTION = 0.1

# Whether to use roulette wheel selection (True) or truncation/elitism
# (False).
ROULETTE_WHEEL_SEL = True

# Number of moves to play in Tetris
MOVE_COUNT = 500

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
    perturb_range = 0.25
    for i in range(len(ch)):
        if randrange(100) < P_MUTATION:
            v = mutate_range
        else:
            v = perturb_range
        ch[i] += -v + 2 * random() * v
    return ch

# Two chromosomes get down and dirty
def mate2(parent1, parent2):
    number_of_genes_from_second_parent = randint(1,len(parent2))
    child1 = parent1[:]
    child2 = parent2[:]
    for i in sample(range(5), k=number_of_genes_from_second_parent):
        child1[i] = parent2[i]
    for i in sample(range(5), k=number_of_genes_from_second_parent):
        child2[i] = parent1[i]
    return mutate(child1), mutate(child2)

def mate(parent1, parent2):
    i = randint(0, len(parent1))
    code1, code2 = parent1[1], parent2[1]
    child_code1 = mutate(code1[:i] + code2[i:])
    child_code2 = mutate(code2[:i] + code1[i:])
    return child_code1, child_code2

def breed_population(pop, fit_fun, higher_better):
    n = len(pop)
    if ROULETTE_WHEEL_SEL:
        # Roulette wheel section based on probabilities. Doesn't seem
        # to converge as quickly as truncation.
        fits = [p[0] for p in pop]
        tot = sum(fits)
        probs = [fit / tot for fit in fits]
    else:
        # Truncation selection.
        pop = sorted(pop)
        if higher_better:
            pop = list(reversed(pop))
        pop = pop[:int(len(pop) * ELITE_FRACTION)]
    pop2 = []
    while len(pop2) < n:
        # We allow self-mating because it is unlikely enough in large
        # populations.
        if ROULETTE_WHEEL_SEL:
            p1, p2 = choices(pop, probs, k = 2)
        else:
            p1, p2 = choices(pop, k = 2)
        # Find two individuals, based on their fitness probability
        # for _ in range(20):
        #     p1, p2 = choices(pop, k = 2) # , probs, k = 2)
        #     if p1 != p2:
        #         break
        if CROSSOVER_TYPE == 'single':
            c1, c2 = mate(p1, p2)
        elif CROSSOVER_TYPE == 'uniform':
            c1, c2 = mate2(p1, p2)
        else:
            print('Wrong crossover type!')
        # Calculate their fitness and insert them in the new
        # population.
        pop2.append((fit_fun(c1), c1))
        pop2.append((fit_fun(c2), c2))
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
    min_fits = min(fits)
    max_fits = max(fits)
    mean_fits = mean(fits)
    stdev_fits = stdev(fits)
    if DEBUG_OUTPUT:
        print(fmt.format(gen,
                         min_fits, mean_fits, max_fits, stdev_fits,
                         items))
    print('[%.3f, %.3f, %.3f],' % (min_fits, mean_fits, max_fits))

def run_evolution(forefather, fitness, n, n_gens, higher_better):
    fmt = '* Running evolution for {0} generations with population size' \
        ' {1}, {2} scores better.'
    s = 'higher' if higher_better else 'lower'
    pop = list(create_population(n, forefather, fitness))
    for gen in range(n_gens):
        generation_stats(gen, pop, higher_better)
        pop = breed_population(pop, fitness, higher_better)

def evolve_tetris():
    from src.environment import TetrisApp
    def tetris_fitness(weights):
        seq = [randint(0, 6) for _ in range(MOVE_COUNT)]
        app = TetrisApp(False, weights)
        return app.runSequenceNoGUI(seq)
    def forefather():
        return [uniform(-10, 10) for _ in range(5)]
    run_evolution(forefather, tetris_fitness, POP_SIZE, N_GENS, True)

if __name__ == '__main__':
    evolve_tetris()
