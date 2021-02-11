from libcpp cimport bool

cdef extern from "kpkc.h":
    cdef cppclass KPartiteKClique:
        KPartiteKClique(bool **, int n_vertices, int* first_per_part, int k)
        KPartiteKClique(bool **, int n_vertices, int* first_per_part, int k, int prec_depth)
        KPartiteKClique()
        bool next()
        const int* k_clique()

    cdef cppclass bitCLQ(KPartiteKClique):
        pass
