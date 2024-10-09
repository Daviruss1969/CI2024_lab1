import numpy as np

# Problem consts (do not edit)
UNIVERSES_SIZE = [100, 1000, 10000, 100000, 100000, 100000]
NUMS_SETS = [10, 100, 1000, 10000, 10000, 10000]
DENSITIES = [0.2, 0.2, 0.2, 0.1, 0.2, 0.3]

# Initialisation
print('Select your instance for the set cover problem :')
print('0) Universe size :100              | Num sets :10                | Density:0.2')
print('1) Universe size :1 000            | Num sets :100               | Density:0.2')
print('2) Universe size :10 000           | Num sets :1 000             | Density:0.2')
print('3) Universe size :100 000          | Num sets :10 000            | Density:0.1')
print('4) Universe size :100 000          | Num sets :10 000            | Density:0.2')
print('5) Universe size :100 000          | Num sets :10 000            | Density:0.3')

index = int(input("Enter problem number (e.g.: 0) : "))

UNIVERSE_SIZE = UNIVERSES_SIZE[index]
NUM_SETS = NUMS_SETS[index]
DENSITY = DENSITIES[index]
SETS = np.random.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
for s in range(UNIVERSE_SIZE):
    if not np.any(SETS[:, s]):
        SETS[np.random.randint(NUM_SETS), s] = True
COSTS = np.pow(SETS.sum(axis=1), 1.1)

def valid(solution: np.ndarray) -> bool:
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.all(np.logical_or.reduce(SETS[solution])) # phenotype

def cost(solution: np.ndarray) -> int:
    """Returns the cost of a solution (to be minimized)"""
    return COSTS[solution].sum()

def fitness(solution: np.ndarray) -> tuple[bool, int]:
    """"Return the fitness of a solution (to be maximized)"""
    return (valid(solution), -cost(solution))

def tweak(solution: np.ndarray, strength: float) -> np.ndarray:
    """tweak function that perform a mutation on n random index according to a probability"""
    mask = np.random.random(NUM_SETS) < strength
    if not np.any(mask):
        mask[np.random.randint(NUM_SETS)] = True
    new_sol = np.logical_xor(solution, mask)
    return new_sol

def set_cover(initial_solution: np.ndarray, max_iterations: int) -> np.ndarray:
    """Perform the set_cover algorithm on a given solution"""
    solution = initial_solution.copy()
    fitness_solution = fitness(solution)
    strength = 0.3
    succes = 0
    c = 0.98
    for i in range(max_iterations):
        if i % (max_iterations // 10) == 0:
            percent_complete = (i / max_iterations) * 100
            print(f"\t{percent_complete:.0f}%")

        if i%5:
            if succes > 1:
                strength/c
            elif succes < 1:
                strength*=c
            succes = 0

        test_solution = tweak(solution, strength)
        fitness_test_solution = fitness(test_solution)
        if fitness_test_solution > fitness_solution:
            solution = test_solution
            fitness_solution = fitness_test_solution
            succes += 1
    return solution

def multiple_set_cover(trials: int, max_iterations: int)-> np.ndarray:
    """Perform multiple time a set_cover algorithm and return the best one"""
    solution = np.random.random(NUM_SETS) < .5
    for i in range(trials):
        print(f'Trial number : {i+1}')
        new_solution = np.random.random(NUM_SETS) < .5
        new_solution = set_cover(new_solution, max_iterations)
        if (fitness(new_solution) > fitness(solution)):
            solution = new_solution
    print()
    return solution

max_iterations = input('Select your number of iteration for the problem (default 5 000) : ')
if max_iterations == '':
    max_iterations = 5_000
else :
    max_iterations = int(max_iterations)

trials = input('Select your number of trials for the problem (default 5) : ')
if trials == '':
    trials = 5
else :
    trials = int(trials)

print()
solution = multiple_set_cover(trials, max_iterations)
solution_fitness = fitness(solution)
print(f'The solution is{"" if solution_fitness[0] else " not"} valid, the final cost is {-solution_fitness[1]}')