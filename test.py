from kpkc.test import get_random_k_partite_graph
from random import random, randint
import cydoctest
import kpkc.kpkc


def _test(k, min_part_size, max_part_size, dens1, dens2):
    print("Testing a graph with {} parts of sizes {} to {} and density between {} and {}".format(
        k, min_part_size, max_part_size, dens1, dens2))
    G = get_random_k_partite_graph(k, min_part_size, max_part_size, dens1, dens2)
    if any(len(part) == 0 for part in G.parts):
        # Check proper error handling
        try:
            list(G.kpkc())
        except ValueError as e:
            if not e.args[0] == "parts may not be empty":
                raise
        try:
            list(G.bitCLQ())
        except ValueError as e:
            if not e.args[0] == "parts may not be empty":
                raise
        return
    G.check()


# The actual tests.

cydoctest.testmod(kpkc.kpkc, verbose=True)

for i in range(2, 7):
    min_part_size = randint(5, 40-4*i)
    max_part_size = min_part_size + randint(0, 40-5*i)
    dens1 = random()
    dens2 = dens1 + (1-dens1)*random()
    _test(i, min_part_size, max_part_size, dens1, dens2)

for i in range(5):
    _test(10, 0, 10, 0.8, 0.9)

for i in range(20):
    _test(10, 0, 5, 0.8, 0.9)

_test(61, 1, 1, 1, 1)
