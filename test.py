from kpkc.test import get_random_k_partite_graph
from random import random, randint
import cydoctest
import kpkc.kpkc

cydoctest.testmod(kpkc.kpkc, verbose=True)

for i in range(2, 7):
    min_part_size = randint(5, 40-4*i)
    max_part_size = min_part_size + randint(0, 40-5*i)
    dens1 = random()
    dens2 = dens1 + (1-dens1)*random()
    print("Testing a graph with {} parts of sizes {} to {} and density between {} and {}".format(
        i, min_part_size, max_part_size, dens1, dens2))
    G = get_random_k_partite_graph(i, min_part_size, max_part_size, dens1, dens2)
    G.check()
