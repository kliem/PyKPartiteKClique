# distutils: include_dirs = kpkc/cppkpkc
# distutils: language = c++
# distutils: extra_compile_args= -std=c++11
from libcpp cimport bool

cdef extern from "cppkpkc/kpkc.cpp":
    cdef cppclass KPartiteKClique:
        void init(bool **, int n_vertices, int* first_per_part, int k) except +
        void init(bool **, int n_vertices, int* first_per_part, int k, int prec_depth) except +
        KPartiteKClique()
        const int* k_clique()

        # Do NOT wrap this in cysignals sig_on/sig_off, it has its own interrupt handling.
        # Its own interrupt handling exits at safe states, so that this can be called again
        # to continue.
        bool next() except +

    cdef cppclass FindClique(KPartiteKClique):
        void init(bool **, int n_vertices, int* first_per_part, int k) except +
        void init(bool **, int n_vertices, int* first_per_part, int k, int prec_depth) except +
        FindClique()
