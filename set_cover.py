import numpy as np

# Problem consts (do not edit)
UNIVERSES_SIZE = [100, 1000, 10000, 100000, 100000, 100000]
NUMS_SETS = [10, 100, 1000, 10000, 10000, 10000]
DENSITIES = [0.2, 0.2, 0.2, 0.1, 0.2, 0.3]

# Consts used to define boundary to the problem (can be edited)
MAXS_ITERATIONS = [50000, 5000, 500, 50, 50, 50]
MAXS_EXPLORATIONS = [15, 10, 5, 2, 2, 2]


def valid(solution: np.ndarray) -> bool:
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.all(np.logical_or.reduce(SETS[solution])) # phenotype

def cost(solution: np.ndarray) -> int:
    """Returns the cost of a solution (to be minimized)"""
    return COSTS[solution].sum()

def fitness(solution: np.ndarray) -> tuple[bool, int]:
    """"Return the fitness of a solution (to be maximized)"""
    return (valid(solution), -cost(solution))

def tweak(solution: np.ndarray, num_sets: int) -> np.ndarray:
    """tweak function that perform a mutation on n random index according to a given probability"""
    mask = np.random.random(num_sets) < 0.01
    new_sol = np.logical_xor(solution, mask)
    return new_sol

def set_cover(initial_solution: np.ndarray, num_sets: int, max_iterations: int, max_explorations: int) -> np.ndarray:
    """Perform the set_cover algorithm on a given solution"""
    solution = initial_solution.copy()
    for _ in range(max_iterations):
        test_solution = tweak(solution, num_sets)
        for _ in range(max_explorations):
            new_solution = tweak(solution, num_sets)
            if (fitness(new_solution) > fitness(test_solution)):
                test_solution = new_solution

        if fitness(test_solution) > fitness(solution):
            solution = test_solution
    return solution

for i in range(6):
    # Get the variables for the current problem
    num_sets = NUMS_SETS[i]
    universe_size = UNIVERSES_SIZE[i]
    density = DENSITIES[i]
    max_iterations = MAXS_ITERATIONS[i]
    max_explorations = MAXS_EXPLORATIONS[i]

    # Initialisation of the sets (transform them into a feasable problem if not)
    SETS = np.random.random((num_sets, universe_size)) < density
    for s in range(universe_size):
        if not np.any(SETS[:, s]):
            SETS[np.random.randint(num_sets), s] = True

    # Compute costs
    COSTS = np.pow(SETS.sum(axis=1), 1.1)

    # Generate initial solutions
    initial_solution = np.full(num_sets, True)

    print(f"Performing the set_cover algorithm for num_sets={num_sets}, universe_size={universe_size}, density={density}, max iterations={max_iterations}, max explorations={max_explorations}")
    print(f"The initial cost is {cost(initial_solution)}")

    final_solution = set_cover(initial_solution, num_sets, max_iterations, max_explorations)
    print(f"The final cost of the solution is {cost(final_solution)}")
    print()