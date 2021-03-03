# distutils: include_dirs = KPartiteKClique
# distutils: language = c++
from libcpp cimport bool

cdef extern from "KPartiteKClique/kpkc.h":
    cdef cppclass KPartiteKClique:
        KPartiteKClique(bool **, int n_vertices, int* first_per_part, int k)
        KPartiteKClique(bool **, int n_vertices, int* first_per_part, int k, int prec_depth)
        KPartiteKClique()
        bool next()
        const int* k_clique()

    cdef cppclass bitCLQ:
        bitCLQ(bool **, int n_vertices, int* first_per_part, int k)
        bitCLQ(bool **, int n_vertices, int* first_per_part, int k, int prec_depth)
        bitCLQ()
        bool next()
        const int* k_clique()
