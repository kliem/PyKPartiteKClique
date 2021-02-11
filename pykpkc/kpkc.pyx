from cysignals.signals cimport sig_on, sig_off
from cysignals.memory cimport check_allocarray, check_reallocarray, check_calloc, sig_free

from _kpkc_memory_allocator cimport MemoryAllocator

def KPartiteKClique_iter(G, parts, int prec_depth=5, benchmark=False):
    """
    Iterates over all k-cliques
    """
    cdef int i, j
    cdef MemoryAllocator mem = MemoryAllocator()
    assert isinstance(parts, list)  # We will allow more flexibility later.

    cdef int k = len(parts)
    cdef int* first_per_part = <int*> mem.allocarray(k, sizeof(int))

    cdef int counter = 0
    for i in range(k):
        first_per_part[i] = counter
        counter += len(parts[i])

    cdef int n = counter

    cdef bool ** incidences = <bool **> mem.allocarray(n, sizeof(bool *))
    for i in range(n):
        incidences[i] = <bool *> mem.calloc(n, sizeof(bool))

    def id_to_part(index):
        for i in range(k):
            if first_per_part[i] > index:
                break
        else:
            i += 1
        i -= 1
        return i

    cdef int* id_to_part_cached = <int*> mem.allocarray(n, sizeof(int))
    for i in range(n):
        id_to_part_cached[i] = id_to_part(i)

    def id_to_vertex(index):
        i = id_to_part_cached[index]
        return parts[i][index - first_per_part[i]]

    cdef dict vertex_to_id = {id_to_vertex(i): i for i in range(n)}

    cdef int ui, vi

    if hasattr(G, "edge_iterator"):
        # G is probably a SageMath graph.
        for u, v in G.edge_iterator(sort_vertices=False, labels=False):
            ui = vertex_to_id[u]
            vi = vertex_to_id[v]
            if id_to_part_cached[ui] == id_to_part_cached[vi]:
                raise ValueError("not a k-partite graph")
            incidences[ui][vi] = True
            incidences[vi][ui] = True
    else:
        for u, v in G:
            ui = vertex_to_id[u]
            vi = vertex_to_id[v]
            if id_to_part_cached[ui] == id_to_part_cached[vi]:
                raise ValueError("not a k-partite graph")
            incidences[ui][vi] = True
            incidences[vi][ui] = True


    if benchmark:
        yield []

    cdef KPartiteKClique * K = new KPartiteKClique(incidences, n, first_per_part, k, prec_depth)

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
