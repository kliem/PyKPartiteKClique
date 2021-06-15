from memory_allocator cimport MemoryAllocator

cdef class KCliqueIterator_base:
    """
    A base class to iterate over all k-clique

    EXAMPLES::

    >>> from kpkc.kpkc import KCliqueIterator_base
    >>> KCliqueIterator_base([[1, 2]], [[1], [2]])
    An iterator over all 2-cliques of a 2-partite graph with 2 vertices

    .. SEEALSO::

        :class:`KPartiteKClique_wrapper`
        :class:`FindClique_wrapper`
    """
    cdef MemoryAllocator mem
    cdef bool **incidences
    cdef int* first_per_part
    cdef int* id_to_part
    cdef int k
    cdef int n
    cdef dict vertex_to_id
    cdef dict id_to_vertex
    cdef const int* k_clique
    cdef KPartiteKClique_base* K

    def __cinit__(self, G, parts, int prec_depth=5):
        cdef int i, j
        self.mem = MemoryAllocator()
        assert isinstance(parts, (list, tuple)), "parts must be a tuple or list"

        self.k = len(parts)
        cdef int k = self.k
        self.first_per_part = <int*> self.mem.allocarray(k + 1, sizeof(int))
        cdef int* first_per_part = self.first_per_part

        cdef int counter = 0
        for i in range(k):
            first_per_part[i] = counter
            counter += len(parts[i])

        self.n = counter
        cdef int n = self.n
        first_per_part[k] = n

        self.incidences = <bool**> self.mem.allocarray(n, sizeof(bool*))
        cdef bool** incidences = self.incidences
        for i in range(n):
            self.incidences[i] = <bool*> self.mem.calloc(n, sizeof(bool))

        self.id_to_part = <int*> self.mem.allocarray(n, sizeof(int))
        cdef int* id_to_part = self.id_to_part
        for i in range(k):
            for j in range(first_per_part[i], first_per_part[i+1]):
                id_to_part[j] = i

        def id_to_vertex(index):
            i = id_to_part[index]
            return parts[i][index - first_per_part[i]]

        self.id_to_vertex = {i: id_to_vertex(i) for i in range(n)}

        self.vertex_to_id = {self.id_to_vertex[i]: i for i in range(n)}

        cdef int ui, vi

        if hasattr(G, "edge_iterator"):
            # G is probably a SageMath graph.
            G = G.edge_iterator(sort_vertices=False, labels=False)

        for u, v in G:
            ui = self.vertex_to_id[u]
            vi = self.vertex_to_id[v]
            if id_to_part[ui] == id_to_part[vi]:
                raise ValueError("not a k-partite graph")
            incidences[ui][vi] = True
            incidences[vi][ui] = True

    def __dealloc__(self):
        del self.K

    def __next__(self):
        cdef bool has_next = self.K.next()
        if has_next:
            self.k_clique = self.K.k_clique()
            return self.make_k_clique()
        else:
            raise StopIteration

    cdef inline list make_k_clique(self):
        cdef int i
        return [self.id_to_vertex[self.k_clique[i]] for i in range(self.k)]

    def __iter__(self):
        return self

    def __repr__(self):
        return "An iterator over all {}-cliques of a {}-partite graph with {} vertices".format(self.k, self.k, self.n)

cdef class KPartiteKClique_wrapper(KCliqueIterator_base):
    """
    Iterate over all k-cliques of a graph using the algorithm ``'kpkc'``.

    This is a depth-first branch and bound algorithm, which picks first
    the vertex with the least edges.

    INPUT:

    - ``G`` -- edges of a k-partite graph
    - ``parts`` -- a list of parts of the graph; each graph has list of nodes
    - ``prec_depth`` -- (default: ``5``); to which depth the pivot shall be precicely determined

    EXAMPLES::

        >>> from kpkc.kpkc import KPartiteKClique_wrapper
        >>> it = KPartiteKClique_wrapper([[1, 3], [2, 3], [1, 4], [2, 4], [1, 5], [2, 6]], [[1, 2], [3, 4, 5, 6]])
        >>> next(it)
        [2, 6]
        >>> next(it)
        [1, 5]
    """

    def __cinit__(self, G, parts, int prec_depth=5):
        self.K = new KPartiteKClique(self.incidences, self.n, self.first_per_part, self.k, prec_depth)

cdef class FindClique_wrapper(KCliqueIterator_base):
    """
    Iterate over all k-cliques of a graph using the algorithm ``'kpkc'``.

    This is a depth-first branch and bound algorithm, which picks first
    the part with the least nodes.

    INPUT:

    - ``G`` -- edges of a k-partite graph
    - ``parts`` -- a list of parts of the graph; each graph has list of nodes
    - ``prec_depth`` -- ignored

    EXAMPLES::

        >>> from kpkc.kpkc import FindClique_wrapper
        >>> it = FindClique_wrapper([[1, 3], [2, 3], [1, 4], [2, 4], [1, 5], [2, 6]], [[1, 2], [3, 4, 5, 6]])
        >>> it = FindClique_wrapper([[1, 3], [2, 3], [1, 4], [2, 4], [1, 5], [2, 6]], [[1, 2], [3, 4, 5, 6]])
        >>> next(it)
        [1, 3]
        >>> next(it)
        [1, 4]
        >>> next(it)
        [1, 5]
        >>> next(it)
        [2, 3]
        >>> next(it)
        [2, 4]
        >>> next(it)
        [2, 6]
    """

    def __cinit__(self, G, parts, int prec_depth=5):
        self.K = new FindClique(self.incidences, self.n, self.first_per_part, self.k)

def KCliqueIterator(*args, algorithm='kpkc', **kwds):
    """
    Iterate over all k-cliques of a graph.

    INPUT:

    - ``G`` -- edges of a k-partite graph
    - ``parts`` -- a list of parts of the graph; each graph has list of nodes
    - ``algorithm`` -- (default: ``'kpkc'``); the algorithm to use; one of ``'kpkc'`` or ``'FindClique'``
    - ``prec_depth`` -- (optional keyword); to which depth the pivot shall be precicely determined

    EXAMPLES::

        >>> from kpkc import KCliqueIterator
        >>> list(KCliqueIterator([[1,2]], [[1], [2]]))
        [[1, 2]]
        >>> edges = [[i, (i+3) % 9] for i in range(9)] + [[i, ((i+4) % 9) if i % 3 != 2 else ((i+1) % 9)] for i in range(9)]
        >>> parts = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        >>> output = list(KCliqueIterator(edges, parts))
        >>> from sys import platform
        >>> platform == "darwin" or output == [[2, 5, 8], [0, 4, 8], [1, 4, 7], [2, 3, 7], [1, 5, 6], [0, 3, 6]]  # output not on mac
        True
        >>> platform != "darwin" or output == [[0, 4, 8], [2, 5, 8], [1, 4, 7], [2, 3, 7], [0, 3, 6], [1, 5, 6]]  # output on mac
        True
        >>> list(KCliqueIterator(edges, parts, algorithm='FindClique'))
        [[0, 3, 6], [0, 4, 8], [1, 4, 7], [1, 5, 6], [2, 3, 7], [2, 5, 8]]

    One may give parts as a list or tuple::

        >>> parts = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
        >>> list(KCliqueIterator(edges, parts, algorithm='FindClique'))
        [[0, 3, 6], [0, 4, 8], [1, 4, 7], [1, 5, 6], [2, 3, 7], [2, 5, 8]]

    """
    if algorithm == 'kpkc':
        return KPartiteKClique_wrapper(*args, **kwds)
    elif algorithm == 'FindClique':
        return FindClique_wrapper(*args, **kwds)
    else:
        raise ValueError("unkown algorithm")
