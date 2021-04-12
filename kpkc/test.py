from random import random, randint
from .kpkc import KCliqueIterator


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

    return kpkcTester(edges, parts)


def get_random_k_partite_graph_2(n_parts, max_part_size, dens):
    r"""
    Generate random k-partite graphs.

    This choice seems more natural for some settings.

    If parts have less choices, those choices are more popular.

    Concretely, the probability of an edge between two vertices of two parts is determined
    by the number of vertices in the smaller part ``l`` by:

    ``1/(largest_part - 1.0) * ( (largest_part - l) + (l - 1.0)*dens)``
    """
    B = list(range(n_parts))
    # Construct nodes
    offset = 0
    sizes = [1 + ((max_part_size - 1) * i)//(n_parts) for i in range(1, n_parts + 1)]
    parts = []
    for b in B:
        parts.append(list(range(offset, offset+sizes[b])))
        offset += sizes[b]

    weights_per_part = [
            (max_part_size - sizes[i]) / (max_part_size - 1.0)
            + (sizes[i] - 1.0) * dens / (max_part_size - 1.0)
            for i in range(n_parts)]

    edges = []

    for b in range(n_parts):
        for i in parts[b]:
            for b1 in range(b+1, n_parts):
                for i1 in parts[b1]:
                    if random() < max(weights_per_part[b], weights_per_part[b1]):
                        edges.append([i, i1])

    return kpkcTester(edges, parts)


class kpkcTester:
    def __init__(self, edges, parts):
        self.edges = edges
        self.parts = parts

    def __repr__(self):
        return "class to test kpkc"

    def benchmark(self, algorithm='kpkc', prec_depth=5, first_only=False):
        from time import time
        if algorithm == 'kpkc':
            it = self.kpkc(prec_depth=prec_depth)
        elif algorithm == 'FindClique':
            it = self.FindClique()
        else:
            it = self.networkx(benchmark=True)
            _ = next(it)

        a = time()
        try:
            _ = next(it)
        except StopIteration:
            b = time()
            yield b-a
            if not first_only:
                yield b-a
            return
        b = time()
        yield b-a
        if first_only:
            return
        c = time()
        sum(1 for _ in it)
        d = time()
        yield d-c + b-a

    def kpkc(self, prec_depth=5):
        it = KCliqueIterator(self.edges, self.parts, prec_depth=prec_depth, algorithm='kpkc')
        return it

    def FindClique(self):
        it = KCliqueIterator(self.edges, self.parts, algorithm='FindClique')
        return it

    def networkx(self, benchmark=False):
        import networkx
        G = networkx.graph.Graph(self.edges)
        if benchmark:
            yield None
        yield from (i for i in networkx.find_cliques(G) if len(i) == len(self.parts))

    def check(self):
        T = set(tuple(sorted(c)) for c in self.networkx())

        def test(it):
            T1 = set(tuple(sorted(c)) for c in it)
            assert T == T1

        test(self.FindClique())
        for i in range(5):
            test(self.kpkc(prec_depth=i))

        print("The tested graph has {} k-cliques".format(len(T)))

    def save(self, filename):
        import gzip
        import json
        data = {'edges': self.edges, 'parts': self.parts}
        with gzip.open(filename, 'w') as fout:
            fout.write(json.dumps(data).encode('utf-8'))


def load_tester(filename):
    import gzip
    import json
    with gzip.open(filename, 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))
    edges = data['edges']
    parts = data['parts']

    # Make vertices hashable again.
    def fix_vertex(v):
        if isinstance(v, list):
            v = tuple(v)
        return v

    def fix_edge_or_part(edge):
        return [fix_vertex(x) for x in edge]

    parts = [fix_edge_or_part(part) for part in data['parts']]
    edges = [fix_edge_or_part(edge) for edge in data['edges']]

    return kpkcTester(edges, parts)


def sage_graph_to_tester(G):
    dic_parts = {v: v[0] for v in G.vertices()}
    values = set(dic_parts.values())
    parts = [[] for _ in values]
    for vertex in dic_parts:
        parts[dic_parts[vertex]].append(vertex)
    return kpkcTester(tuple(G.edge_iterator(sort_vertices=False, labels=False)), parts)
