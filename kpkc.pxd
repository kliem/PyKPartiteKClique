# distutils: depends = KPartiteKClique/kpkc.cpp KPartiteKClique/kpkc.h
# distutils: include_dirs = KPartiteKClique
# distutils: sources = KPartiteKClique/kpkc.cpp
# distutils: extra_compile_args=-O3 -march=native -std=c++11
# distutils: language = c++

from libcpp cimport bool

cdef extern from "kpkc.h":
    cdef cppclass KPartiteKClique:
        KPartiteKClique(bool **, int n_vertices, int* first_per_part, int k)
        KPartiteKClique()
        bool next()
        const int* k_clique()
