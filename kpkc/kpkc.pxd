# distutils: include_dirs = kpkc/cppkpkc
# distutils: language = c++
# distutils: extra_compile_args= -std=c++11
from libcpp cimport bool

cdef extern from "cppkpkc/kpkc.cpp":
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