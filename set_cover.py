from icecream import ic
from typing import Callable
import numpy as np
# Const
UNIVERSE_SIZE = 10000
NUM_SETS = 1000
DENSITY = 0.1
MAX_ITERATIONS = 1000

# Initialisatino of the sets (transform them into a feasable problem if not)
SETS = np.random.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
for s in range(UNIVERSE_SIZE):
    if not np.any(SETS[:, s]):
        SETS[np.random.randint(NUM_SETS), s] = True

# Compute costs
COSTS = np.pow(SETS.sum(axis=1), 1.1)


def valid(solution: np.ndarray) -> bool:
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.all(np.logical_or.reduce(SETS[solution])) # phenotype

def cost(solution) -> int:
    """Returns the cost of a solution (to be minimized)"""
    return COSTS[solution].sum()

def fitness(solution: np.ndarray) -> tuple[bool, int]:
    """"Return the fitness of a solution (to be maximized)"""
    return (valid(solution), -cost(solution))

def single_mutation(solution: np.ndarray) -> np.ndarray:
    """1st tweak function that perform a mutation on one random index"""
    new_sol = solution.copy()
    index = np.random.randint(NUM_SETS)
    new_sol[index] = not new_sol[index]
    return new_sol

def multiple_mutation(solution: np.ndarray) -> np.ndarray:
    """2nd tweak function that perform a mutation on n random index according to a given probability"""
    mask = np.random.random(NUM_SETS) < 0.01
    new_sol = np.logical_xor(solution, mask)
    return new_sol

def set_cover(initial_solution: np.ndarray, tweak: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
    """Perform the set_cover algorithm on a given solution with a given tweak"""
    solution = initial_solution.copy()
    for _ in range(MAX_ITERATIONS):
        new_solution = tweak(solution)
        if fitness(new_solution) > fitness(solution):
            solution = new_solution
    return solution

# Generate initial solutions
solution = np.full(NUM_SETS, True)

# Single mutation
final_solution = set_cover(solution, single_mutation)
ic(final_solution)
ic(fitness(final_solution))

# Multiple mutation
final_solution = set_cover(solution, multiple_mutation)
ic(final_solution)
ic(fitness(final_solution))