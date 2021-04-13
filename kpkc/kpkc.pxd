# distutils: include_dirs = kpkc/cppkpkc
# distutils: language = c++
# distutils: extra_compile_args= -std=c++11
from libcpp cimport bool

cdef extern from "cppkpkc/kpkc.cpp":
    cdef cppclass KPartiteKClique:
        void init(bool **, int n_vertices, int* first_per_part, int k) except +
        void init(bool **, int n_vertices, int* first_per_part, int k, int prec_depth) except +
        KPartiteKClique()
        bool next() except +
        const int* k_clique()

    cdef cppclass FindClique(KPartiteKClique):
        void init(bool **, int n_vertices, int* first_per_part, int k) except +
        void init(bool **, int n_vertices, int* first_per_part, int k, int prec_depth) except +
        FindClique()
