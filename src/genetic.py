import random
def obj_func(coded_string):
    return random.randint(1,100)


def create_initial_population(size_of_initial_population, coded_string_length):
    population = [(random.sample(range(1,20),coded_string_length)) for _ in range(size_of_initial_population)]
    for i in range(len(population)):
        population[i].sort()
    return population

def obj_func(individual):

    return random.randint(1,10)

def select(individuals, select_this_many):
    objective_values = [obj_func(element) for element in individuals]
    probabilities = [objective_values[i]/sum(objective_values) for i in range(len(objective_values))]

    return probabilities


def optimize_it():
    population = create_initial_population()
    best_objective_value = 99999
    iteration = 0
    index_of_it = None
    while(best_objective_value>1000 and iteration<100):
        individuals = select(individuals)
        
        individuals = create_offspring(individuals)
        
        individuals = mutate(individuals)
        
        best_objective_value, index_of_it = compute_best_objective_value(individuals)
       
        iteration +=1
    
