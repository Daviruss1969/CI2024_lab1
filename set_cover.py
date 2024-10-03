from random import random, seed
from itertools import product
import numpy as np

from icecream import ic

UNIVERSE_SIZE = 100
NUM_SETS = 10
DENSITY = 0.2

def valid(solution):
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.all(np.logical_or.reduce(SETS[solution]))

def cost(solution):
    """Returns the cost of a solution (to be minimized)"""
    return COSTS[solution].sum()

# rng = np.random.Generator(np.random.PCG64([UNIVERSE_SIZE, NUM_SETS, int(10_000 * DENSITY)]))


# Initialisation
SETS = np.random.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
# Transform to a feasable problem if not
for s in range(UNIVERSE_SIZE):
    if not np.any(SETS[:, s]):
        SETS[np.random.randint(NUM_SETS), s] = True
COSTS = np.power(SETS.sum(axis=1), 1.1)