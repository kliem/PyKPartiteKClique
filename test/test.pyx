# distutils: include_dirs = PyKPartiteKClique/kpkc/KPartiteKClique PyKPartiteKClique/kpkc
from cysignals.signals cimport sig_on, sig_off
from kpkc.kpkc cimport *

from kpkc.memory_allocator cimport MemoryAllocator

def KPartiteKClique_iter(G, parts, int prec_depth=5, algorithm='kpkc', benchmark=False):
    """
    Iterates over all k-cliques

    INPUT:

    EXAMPLES::

        >>> from kpkc.kpkc import KPartiteKClique_iter
        >>> list(KPartiteKClique_iter([[1,2]], parts=[[1], [2]]))
        [[1, 2]]
        >>> edges = [[i, (i+3) % 9] for i in range(9)] + [[i, ((i+4) % 9) if i % 3 != 2 else ((i+1) % 9)] for i in range(9)]
        >>> list(KPartiteKClique_iter(edges, parts=[[0,1,2], [3,4,5], [6,7,8]]))
        [[2, 5, 8], [0, 4, 8], [1, 4, 7], [2, 3, 7], [1, 5, 6], [0, 3, 6]]
        >>> list(KPartiteKClique_iter(edges, parts=[[0,1,2], [3,4,5], [6,7,8]], algorithm='bitCLQ'))
        [[0, 3, 6], [0, 4, 8], [1, 4, 7], [1, 5, 6], [2, 3, 7], [2, 5, 8]]

    The option ``benchmark=True`` yields an empty list first,
    to allow excluding the python overhead from benchmarking::

        >>> list(KPartiteKClique_iter(edges, parts=[[0,1,2], [3,4,5], [6,7,8]], algorithm='bitCLQ', benchmark=True))
        [[], [0, 3, 6], [0, 4, 8], [1, 4, 7], [1, 5, 6], [2, 3, 7], [2, 5, 8]]

    One may give parts as a list or tuple::

        >>> list(KPartiteKClique_iter(edges, parts=((0,1,2), (3,4,5), (6,7,8)), algorithm='bitCLQ', benchmark=True))
        [[], [0, 3, 6], [0, 4, 8], [1, 4, 7], [1, 5, 6], [2, 3, 7], [2, 5, 8]]

    """
    cdef int i, j
    cdef MemoryAllocator mem = MemoryAllocator()

    assert isinstance(parts, (list, tuple)), "parts must be a tuple or list"

    cdef int k = len(parts)
    cdef int* first_per_part = <int*> mem.allocarray(k + 1, sizeof(int))

    cdef int counter = 0
    for i in range(k):
        first_per_part[i] = counter
        counter += len(parts[i])

    cdef int n = counter
    first_per_part[k] = n

    cdef bool** incidences = <bool**> mem.allocarray(n, sizeof(bool*))
    for i in range(n):
        incidences[i] = <bool*> mem.calloc(n, sizeof(bool))

    cdef int* id_to_part = <int*> mem.allocarray(n, sizeof(int))
    for i in range(k):
        for j in range(first_per_part[i], first_per_part[i+1]):
            id_to_part[j] = i

    def id_to_vertex(index):
        i = id_to_part[index]
        return parts[i][index - first_per_part[i]]

    cdef dict vertex_to_id = {id_to_vertex(i): i for i in range(n)}

    cdef int ui, vi

    if hasattr(G, "edge_iterator"):
        # G is probably a SageMath graph.
        G = G.edge_iterator(sort_vertices=False, labels=False)

    for u, v in G:
        ui = vertex_to_id[u]
        vi = vertex_to_id[v]
        if id_to_part[ui] == id_to_part[vi]:
            raise ValueError("not a k-partite graph")
        incidences[ui][vi] = True
        incidences[vi][ui] = True

    if benchmark:
        # We will yield here.
        # This allows ignoring the python overhead for benchmarking.
        yield []

    cdef KPartiteKClique* K
    cdef bitCLQ* K1

    if algorithm == 'kpkc':
        K = new KPartiteKClique(incidences, n, first_per_part, k, prec_depth)

        try:
            sig_on()
            foo = K.next()
            sig_off()
            while foo:
                yield [id_to_vertex(K.k_clique()[i]) for i in range(k)]
                sig_on()
                foo = K.next()
                sig_off()
        finally:
            del K

    elif algorithm == 'bitCLQ':
        K1 = new bitCLQ(incidences, n, first_per_part, k, prec_depth)

        try:
            sig_on()
            foo = K1.next()
            sig_off()
            while foo:
                yield [id_to_vertex(K1.k_clique()[i]) for i in range(k)]
                sig_on()
                foo = K1.next()
                sig_off()
        finally:
            del K1
    else:
        raise ValueError("unkown algorithm")
