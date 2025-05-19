import random
import copy




# configuration
NUM_GENERATIONS = 10 # generations
POPULATION_SIZE = 8 # population size of individuals
MUTATION_RATE = 0.25 # likelyhood of changing mutating a parameter  
ITERATIONS_INDIVIDUAL = 50 # amount of steps in simulation


# Individets parametere
PARAM_RANGES = {
    "new_vaccines": (0, 15),
    "new_patients": (0, 15),
    "m": (0.01, 0.1),
    "cd": (0.005, 0.1),
}

MUTATION_RANGES = {
    "new_vaccines": (0, 4),
    "new_patients": (0, 4),
    "m": (0.01, 0.05),
    "cd": (0.005, 0.02),
}

def initialize_individual():
    """Lager et tilfeldig individ med gyldige parameterverdier."""
    ind = {
        "new_vaccines": random.randint(0, 1),
        "new_patients": random.randint(0, 1),
        "m": round(random.uniform(0.08, 0.1), 4),
        "cd": round(random.uniform(0.5, 0.1), 4),
    }
    ind["cdsq"] = round(ind["cd"] ** 2, 6)
    return ind

def mutate(ind):
    """Muterer et individ ved å endre noen parametere tilfeldig."""
    new_ind = copy.deepcopy(ind)
    for key in ["new_vaccines", "new_patients", "m", "cd"]:
        if random.random() < MUTATION_RATE:
            mutation_range = random.uniform(MUTATION_RANGES[key][0], MUTATION_RANGES[key][1])
            span = (PARAM_RANGES[key][1] - PARAM_RANGES[key][0]) * mutation_range
            delta = random.uniform(-span, span)
            new_val = new_ind[key] + delta
            new_val = max(PARAM_RANGES[key][0], min(PARAM_RANGES[key][1], new_val))
            new_ind[key] = type(ind[key])(round(new_val, 4))
    new_ind["cdsq"] = round(new_ind["cd"] ** 2, 6)
    return new_ind

def crossover(parent1, parent2):
    """Bytter noen av parameterne mellom to foreldre."""
    child = {}
    for key in ["new_vaccines", "new_patients", "m", "cd"]:
        child[key] = random.choice([parent1[key], parent2[key]])
    child["cdsq"] = round(child["cd"] ** 2, 6)
    return child


def select_parents(population, scores):
    """Roulette wheel selection: dårligere individer har lavere sjanse."""
    total = sum([1 / (1 + s) for s in scores])
    probs = [(1 / (1 + s)) / total for s in scores]
    parents = random.choices(population, weights=probs, k=2)
    return parents

