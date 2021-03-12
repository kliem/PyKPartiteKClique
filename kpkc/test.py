from random import random, randint
from .kpkc import KPartiteKClique_iter


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


class kpkcTester:
    def __init__(self, edges, parts):
        self.edges = edges
        self.parts = parts

    def __repr__(self):
        return "class to test kpkc"

    def benchmark(self, algorithm='kpkc', prec_depth=5, first_only=False):
        from time import time
        if algorithm == 'kpkc':
            it = self.kpkc(prec_depth=prec_depth, benchmark=True)
        elif algorithm == 'bitCLQ':
            it = self.bitCLQ(benchmark=True)
        else:
            it = self.networkx(benchmark=True)

        # Construct the cpp-class.
        _ = next(it)

        a = time()
        try:
            _ = next(it)
        except StopIteration:
            b = time()
            if first_only:
                return b-a
            return b-a, b-a
        b = time()
        if first_only:
            return b-a
        sum(1 for _ in it)
        c = time()
        return b-a, c - a

    def kpkc(self, prec_depth=5, benchmark=False):
        it = KPartiteKClique_iter(self.edges, self.parts, benchmark=benchmark, prec_depth=prec_depth, algorithm='kpkc')
        return it

    def bitCLQ(self, benchmark=False):
        it = KPartiteKClique_iter(self.edges, self.parts, benchmark=benchmark, algorithm='bitCLQ')
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

        test(self.bitCLQ())
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
