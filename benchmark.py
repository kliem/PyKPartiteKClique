from time import time
from random import random, randint
from kpkc.kpkc import *

def get_random_k_partite_graph(n_parts, min_part_size, max_part_size, dens1, dens2):
    r"""
    Randomly generated k-partite graphs according to Grünert et al.
    """
    B = list(range(n_parts))
    # Construct nodes
    offset = 0
    sizes = [randint(min_part_size, max_part_size) for _ in range(n_parts)]
    parts = []
    for b in B:
        parts.append(list(range(offset, offset+sizes[b])))
        offset += sizes[b]

    vertex_weight_generators = [dens1 + random()*(dens2 - dens1) for _ in range(offset)]

    edges = []

    for b in range(n_parts):
        for i in parts[b]:
            for b1 in range(b+1, n_parts):
                for i1 in parts[b1]:
                    if random() < (vertex_weight_generators[i] + vertex_weight_generators[i1])/2:
                        edges.append([i, i1])

    return edges, parts

def benchmark_random(*args, prec_depth=5, algorithm='kpkc', first_only=False):
    G, parts = get_random_k_partite_graph(*args)
    return _benchmark(G, parts, prec_depth=prec_depth, algorithm=algorithm, first_only=first_only)

def test_random(*args, prec_depth=5, algorithm='kpkc'):
    G, parts = get_random_k_partite_graph(*args)
    from sage.graphs.all import Graph
    G = Graph(G)
    it = KPartiteKClique_iter(G, parts, prec_depth=prec_depth, algorithm=algorithm)
    a = list(it)
    a = sorted(sorted(x) for x in a)
    b = sorted([sorted(c) for c in G.cliques_maximal() if len(c) == len(parts)])
    assert a == b, (a,b)
    print(len(a))

def benchmark_sample(G, prec_depth=5, algorithm='kpkc', first_only=False):
    dic_parts = {v: v[0] for v in G.vertices()}
    values = set(dic_parts.values())
    parts = [[] for _ in values]
    for vertex in dic_parts:
        parts[dic_parts[vertex]].append(vertex)

    return _benchmark(G, parts, prec_depth=prec_depth, algorithm=algorithm, first_only=first_only)

def _benchmark(*args, prec_depth=5, algorithm='kpkc', first_only=False):
    it = KPartiteKClique_iter(*args, benchmark=True, prec_depth=prec_depth, algorithm=algorithm)
    _ = next(it)
    a = time()
    try:
        _ = next(it)
    except StopIteration:
        b = time()
        return b-a, b-a
    b = time()
    if first_only:
        return b-a
    sum(1 for _ in it)
    c = time()
    return b-a, c - a
