from sage.all import *
from time import time

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

    G = Graph()
    G.add_vertices(range(sum(sizes)))

    for b in range(n_parts):
        for i in parts[b]:
            for b1 in range(b+1, n_parts):
                for i1 in parts[b1]:
                    if random() < (vertex_weight_generators[i] + vertex_weight_generators[i1])/2:
                        G.add_edge([i,i1])

    return G, parts

def benchmark_random(*args):
    G, parts = get_random_k_partite_graph(*args)
    return _benchmark(G, parts)

def test_random(*args):
    G, parts = get_random_k_partite_graph(*args)
    it = KPartiteKClique_iter(G, parts)
    a = sorted(list(it))
    b = sorted([c for c in G.cliques_maximal() if len(c) == len(parts)])
    assert a == b
    print(len(a))

def benchmark_sample(G):
    dic_parts = {v: v[0] for v in G.vertices()}
    values = set(dic_parts.values())
    parts = [[] for _ in values]
    for vertex in dic_parts:
        parts[dic_parts[vertex]].append(vertex)

    return _benchmark(G, parts)

def _benchmark(*args):
    it = KPartiteKClique_iter(*args, benchmark=True)
    _ = next(it)
    a = time()
    try:
        _ = next(it)
    except StopIteration:
        b = time()
        return b-a, b-a
    b = time()
    sum(1 for _ in it)
    c = time()
    return b-a, c - a
