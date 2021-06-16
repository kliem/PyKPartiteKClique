# PyKPartiteKClique

A python wrapper of https://github.com/kliem/KPartiteKClique.

Iterate over all k-cliques of a k-partite graph.

## Requirements

- `setuptools`
- `Cython`

## Quick start

A trivial example:

    >>> from kpkc import KCliqueIterator
    >>> edges = [[1, 2]]
    >>> parts = [[1], [2]]
    >>> it = KCliqueIterator(edges, parts)
    >>> list(it)
    [[1, 2]]

The default algorithm is `kpkc`, which first selects nodes with few
edges:

    >>> parts = [[1, 2, 3, 4], [5, 6, 7, 8, 9]]
    >>> edges = [[1, 6], [5, 2], [5, 3]]
    >>> edges += [[i, j] for i in range(2, 5) for j in range(6, 10)]
    >>> it = KCliqueIterator(edges, parts)
    >>> list(it)[:3]
    [[1, 6], [3, 5], [2, 5]]

The algorithm `FindClique` first selects parts with few nodes:

    >>> parts = [[1, 2, 3, 4], [5, 6, 7, 8, 9]]
    >>> edges = [[1, 6], [5, 2], [5, 3]]
    >>> edges += [[i, j] for i in range(2, 5) for j in range(6, 10)]
    >>> it = KCliqueIterator(edges, parts, algorithm='FindClique')
    >>> list(it)
    [[1, 6], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [4, 6], [4, 7], [4, 8], [4, 9]]

## Benchmarks

We benchmark the following algorithms/implementations:

- `kpkc` (our implementation)
- `FindClique` (our implementation)
- `Cliquer` (exposed via `SageMath`)
- `networkx`
- `mcqd` (exposed via `SageMath`)

For this we use three types of graphs:

- Graphs in `sample_graphs/` that can be tested with
`kpkc.test.load_tester`.
- Also we benchmark random graphs with parameters `(k, min_s, max_s, a_1, a_2)`,
  where `k` is the number of parts,
  each part has size in `[min_s, max_s]` chosen with uniform distribution.
  Each vertex `v` is assigned a random float `p(v)` chosen with uniform
  distribution from `[a_1, a_2]`.
  For all pairs `v`, `w` from different parts the edge is generated with
  probability `(p(v) + p(w))/2`.

  This approach is described in:

  - Grunert, Tore & Irnich, Stefan & Zimmermann, Hans-Jürgen & Schneider, Markus & Wulfhorst, Burkhard. (2001). Cliques in k-partite Graphs and their Application in Textile Engineering

  Such a random graph can be obtain with
  `kpkc.test.get_random_k_partite_graph(k, min_s, max_s, a_1, a_2)`.
- In addition we benchmark examples with paramters `(k, max_s, a)`,
  where `k` is the number of parts.
  Parts have sizes `1 + ((max_s -1) * i) // k` for `i` in 1, ..., k.

  Let `f` be the affine function determined by `f(1) = 1` and `f(a) =
  max_s`.
  For all pairs `v`, `w` from different parts with sizes `s`, `t`,
  the edge is generated with probability `f(min(s, t))`.

  This means parts of size 1 will have all neighbors and the more
  vertices a part has, the lower will be the density of its edges.

  Such a random graph can be obtain with
  `kpkc.test.get_random_k_partite_graph_2(k, max_s, a)`.

  In many contexts this might be a more natural choice than the above
  random graph. If the k-clique corresponds to some matching, than
  this corresponds to the fact that fewer choices means that people will
  be less picky. Example:

  Suppose there is only one cement mill in the area, two concrete
  pumps, twenty conrete mixer trucks, and twenty concrete crews.
  Nobody can question the quality of the cement mill, because there is
  no alternative.
  As there is only two concrete pumps, the truck drivers will usually
  be willing to work with both of them.
  Likewise the concrete crews will usually put up with both pump
  operators.
  However, it is very much possible that the conrete crews might refuse
  to work with some truck drivers (always late) or the truck drivers
  might refuse to work with some crews (always order more trucks than
  they need).

  In particular, the graphs in `sample_graphs/` behave somewhat like
  this:
  Vertices in smaller parts have more neighbors than vertices in larger
  parts.
  There are more than 14 million of those that we would like to
  check. This is feasible with `kpkc` and appears infeasible with the
  other implementations.

The results have been obtained with an Intel i7-7700 CPU @3.60GHz.

### Checking for a k-clique

We time how long it takes to either determine the clique number or to
find the first k-clique, if any.

Note that the graphs in `sample_graphs` do not have k-cliques.

`nan` indicates that the computation was interrupted after 1000s (without
determination).

| Graph                       | kpkc       | FindClique | networkx   | Cliquer    | mcqd       |
  ---                         | ---        | ---        | ---        | ---        | ---
| 0                           | 1.67e+01   | nan        | nan        | nan        | nan        |
| 1                           | 1.70e+01   | nan        | nan        | nan        | nan        |
| 2                           | 1.67e+01   | nan        | nan        | nan        | nan        |
| 20                          | 4.52e+00   | nan        | nan        | nan        | nan        |
| 100                         | 1.67e+01   | nan        | nan        | nan        | nan        |
| 1000                        | 2.32e-01   | 7.47e+00   | nan        | nan        | 1.40e+01   |
| 10000                       | 7.60e-02   | 3.23e+00   | nan        | nan        | 4.53e+00   |
| 1000000                     | 1.35e+00   | nan        | nan        | nan        | nan        |
| 2000000                     | 6.50e-02   | 7.60e-01   | nan        | 1.35e+01   | 3.45e+00   |
| 5000000                     | 1.56e-01   | 6.25e+00   | nan        | nan        | 1.44e+01   |
| 10000000                    | 1.65e-02   | 1.61e-04   | nan        | 1.19e+00   | 7.88e-01   |
| (5, 50, 50, 0.14, 0.14)     | 2.00e-05   | 5.72e-06   | 1.46e-03   | 1.35e-03   | 2.09e-03   |
| (5, 50, 50, 0.15, 0.15)     | 6.75e-04   | 2.79e-05   | 1.20e-02   | 1.42e-03   | 1.23e-03   |
| (5, 50, 50, 0.2, 0.2)       | 1.29e-05   | 3.10e-06   | 1.47e-03   | 1.69e-03   | 1.55e-03   |
| (5, 50, 50, 0.25, 0.25)     | 1.34e-05   | 4.05e-06   | 1.43e-03   | 2.22e-03   | 2.02e-03   |
| (5, 50, 50, 0.0, 0.3)       | 9.18e-05   | 7.87e-06   | 1.60e-03   | 1.39e-03   | 1.55e-03   |
| (5, 50, 50, 0.0, 0.4)       | 5.10e-05   | 4.53e-06   | 1.48e-03   | 1.83e-03   | 1.74e-03   |
| (5, 50, 50, 0.0, 0.45)      | 3.08e-05   | 3.58e-06   | 1.25e-03   | 2.20e-03   | 2.08e-03   |
| (5, 50, 50, 0.0, 0.5)       | 2.26e-05   | 4.29e-06   | 1.42e-03   | 2.19e-03   | 2.17e-03   |
| (10, 26, 37, 0.49, 0.49)    | 4.58e-04   | 9.11e-05   | 8.07e-01   | 3.28e-02   | 3.17e-02   |
| (10, 26, 37, 0.5, 0.5)      | 9.91e-04   | 4.03e-05   | 1.50e-01   | 5.11e-02   | 3.85e-02   |
| (10, 26, 37, 0.51, 0.51)    | 1.20e-03   | 1.86e-05   | 3.31e-02   | 4.27e-02   | 3.96e-02   |
| (10, 26, 37, 0.4, 0.6)      | 1.91e-03   | 1.43e-05   | 3.05e-01   | 1.05e-01   | 4.59e-02   |
| (10, 26, 37, 0.3, 0.7)      | 1.74e-04   | 1.53e-05   | 5.43e-03   | 1.26e-01   | 5.12e-02   |
| (10, 50, 50, 0.42, 0.42)    | 1.04e-01   | 1.70e-03   | 2.26e+01   | 2.61e-01   | 1.45e-01   |
| (10, 50, 50, 0.43, 0.43)    | 2.23e-02   | 1.18e-03   | 7.89e+00   | 1.84e-01   | 1.26e-01   |
| (10, 50, 50, 0.44, 0.44)    | 2.57e-02   | 4.64e-04   | 2.13e+00   | 1.96e-01   | 1.65e-01   |
| (10, 50, 50, 0.46, 0.46)    | 4.98e-03   | 2.03e-05   | 8.41e-02   | 3.64e-01   | 2.46e-01   |
| (10, 50, 50, 0.48, 0.48)    | 1.26e-03   | 5.72e-06   | 2.65e-02   | 7.82e-01   | 4.04e-01   |
| (10, 50, 50, 0.5, 0.5)      | 3.91e-04   | 2.10e-05   | 1.41e-02   | 1.40e+00   | 6.94e-01   |
| (50, 5, 15, 0.91, 0.91)     | nan        | 2.07e-01   | nan        | nan        | nan        |
| (50, 5, 15, 0.918, 0.918)   | nan        | 3.04e-01   | nan        | nan        | nan        |
| (50, 5, 15, 0.92, 0.92)     | nan        | 1.34e-01   | nan        | nan        | nan        |
| (20, 23, 39, 0.7, 0.7)      | 3.29e+02   | 2.09e-01   | nan        | nan        | nan        |
| (20, 23, 39, 0.71, 0.71)    | 1.55e+01   | 2.63e-02   | nan        | nan        | nan        |
| (20, 23, 39, 0.72, 0.72)    | 5.09e+00   | 1.74e-03   | nan        | nan        | nan        |
| (20, 23, 39, 0.7, 0.73)     | 2.44e+01   | 5.84e-02   | nan        | nan        | nan        |
| (20, 23, 39, 0.65, 0.78)    | 8.93e-01   | 2.88e-03   | nan        | nan        | nan        |
| (30, 11, 30, 0.6, 0.6)      | 3.03e-01   | 1.10e-04   | nan        | 1.77e+02   | 5.15e+01   |
| (30, 11, 30, 0.7, 0.7)      | 5.13e+00   | 9.04e-04   | nan        | nan        | nan        |
| (30, 11, 30, 0.8, 0.8)      | nan        | 1.63e-01   | nan        | nan        | nan        |
| (30, 11, 30, 0.81, 0.81)    | nan        | 5.80e-01   | nan        | nan        | nan        |
| (30, 11, 30, 0.82, 0.82)    | nan        | 1.42e-01   | nan        | nan        | nan        |
| (30, 11, 30, 0.84, 0.84)    | 7.06e+02   | 7.20e-04   | nan        | nan        | nan        |
| (30, 11, 30, 0.88, 0.88)    | 2.75e+00   | 1.14e-05   | 7.87e+02   | nan        | nan        |
| (100, 10, 10, 0.7, 0.7)     | 4.90e-02   | 5.39e-05   | nan        | nan        | nan        |
| (100, 10, 10, 0.8, 0.8)     | 4.12e+00   | 3.08e-04   | nan        | nan        | nan        |
| (100, 10, 10, 0.85, 0.85)   | 2.36e+02   | 2.50e-03   | nan        | nan        | nan        |
| (100, 10, 10, 0.9, 0.9)     | nan        | 1.43e-01   | nan        | nan        | nan        |
| (100, 10, 10, 0.92, 0.92)   | nan        | 5.80e+00   | nan        | nan        | nan        |
| (100, 10, 10, 0.94, 0.94)   | nan        | nan        | nan        | nan        | nan        |
| (100, 10, 10, 0.95, 0.95)   | nan        | nan        | nan        | nan        | nan        |
| (100, 10, 10, 0.97, 0.97)   | nan        | 8.58e-05   | nan        | nan        | nan        |
| (3, 100, 100, 0.1, 0.1)     | 1.05e-05   | 2.86e-06   | 9.32e-04   | 1.20e-03   | 1.16e-03   |
| (4, 100, 100, 0.15, 0.15)   | 1.67e-05   | 3.10e-06   | 2.17e-03   | 3.41e-03   | 3.34e-03   |
| (5, 100, 100, 0.2, 0.2)     | 2.77e-05   | 3.10e-06   | 4.79e-03   | 7.17e-03   | 8.46e-03   |
| (6, 100, 100, 0.25, 0.25)   | 1.78e-04   | 4.53e-06   | 9.87e-03   | 1.98e-02   | 2.28e-02   |
| (7, 50, 50, 0.35, 0.35)     | 2.87e-04   | 8.11e-06   | 5.90e-03   | 1.11e-02   | 1.09e-02   |
| (8, 50, 50, 0.4, 0.4)       | 1.09e-04   | 1.50e-05   | 9.39e-03   | 3.45e-02   | 3.21e-02   |
| (9, 50, 50, 0.45, 0.45)     | 8.06e-04   | 9.30e-06   | 1.95e-02   | 5.15e-02   | 1.27e-01   |
| (10, 50, 50, 0.5, 0.5)      | 2.76e-03   | 6.44e-06   | 1.71e-02   | 1.85e+00   | 6.71e-01   |
| (10, 10, 10, 0.74, 0.74)    | 4.67e-05   | 3.58e-06   | 1.39e-03   | 8.95e-03   | 3.46e-03   |
| (20, 12, 12, 0.86, 0.86)    | 1.33e-03   | 8.11e-06   | 5.76e-01   | nan        | 3.54e+02   |
| (30, 13, 13, 0.91, 0.91)    | 1.12e-02   | 1.03e-05   | 9.35e-01   | nan        | nan        |
| (40, 13, 13, 0.93, 0.93)    | 1.54e+00   | 1.62e-05   | nan        | nan        | nan        |
| (50, 14, 14, 0.94, 0.94)    | 5.49e-01   | 2.10e-05   | nan        | nan        | nan        |
| (60, 14, 14, 0.95, 0.95)    | nan        | 2.62e-05   | nan        | nan        | nan        |
| (70, 14, 14, 0.96, 0.96)    | 2.94e+02   | 4.46e-05   | nan        | nan        | nan        |
| (10, 22, 22, 0.65, 0.65)    | 1.66e-04   | 4.77e-06   | 3.45e-03   | 3.04e-01   | 1.18e-01   |
| (20, 28, 28, 0.82, 0.82)    | 1.56e-02   | 7.63e-06   | 9.54e-02   | nan        | nan        |
| (30, 31, 31, 0.87, 0.87)    | 3.39e-01   | 1.31e-05   | 3.46e+00   | nan        | nan        |
| (10, 48, 48, 0.59, 0.59)    | 8.51e-05   | 5.25e-06   | 1.20e-02   | 1.25e+01   | 6.54e+00   |
| (20, 68, 68, 0.77, 0.77)    | 2.06e-03   | 9.78e-06   | 5.49e-01   | nan        | nan        |
| (5, 10, 0.1)                | 6.68e-06   | 2.86e-06   | 1.09e-04   | 8.32e-05   | 9.68e-05   |
| (5, 10, 0.2)                | 6.20e-06   | 2.62e-06   | 9.92e-05   | 7.32e-05   | 9.39e-05   |
| (5, 20, 0.05)               | 8.58e-06   | 2.86e-06   | 2.70e-04   | 2.49e-04   | 2.60e-04   |
| (5, 20, 0.1)                | 7.39e-06   | 2.86e-06   | 2.43e-04   | 2.01e-04   | 2.50e-04   |
| (5, 50, 0.01)               | 1.24e-05   | 2.62e-06   | 9.68e-04   | 1.05e-03   | 1.16e-03   |
| (5, 50, 0.02)               | 1.24e-05   | 3.10e-06   | 9.86e-04   | 1.04e-03   | 1.17e-03   |
| (10, 10, 0.4)               | 1.60e-05   | 3.58e-06   | 5.64e-04   | 2.22e-04   | 2.97e-04   |
| (10, 10, 0.6)               | 1.48e-05   | 3.34e-06   | 3.97e-04   | 2.64e-04   | 3.19e-04   |
| (10, 20, 0.3)               | 2.41e-05   | 3.81e-06   | 1.02e-03   | 8.73e-04   | 1.02e-03   |
| (10, 20, 0.5)               | 2.38e-05   | 3.81e-06   | 1.08e-03   | 1.01e-03   | 2.85e-03   |
| (10, 50, 0.05)              | 8.39e-05   | 4.05e-06   | 4.54e-03   | 4.47e-03   | 5.15e-03   |
| (10, 50, 0.1)               | 6.22e-05   | 5.01e-06   | 5.67e-03   | 4.50e-03   | 5.47e-03   |
| (10, 100, 0.01)             | 7.58e-05   | 6.20e-06   | 2.03e-02   | 2.18e-02   | 2.54e-02   |
| (10, 100, 0.02)             | 6.20e-05   | 8.34e-06   | 1.60e-02   | 2.04e-02   | 2.63e-02   |
| (20, 10, 0.6)               | 4.68e-04   | 2.88e-05   | 4.07e+00   | 2.04e-03   | 3.26e-03   |
| (20, 10, 0.7)               | 8.51e-05   | 5.25e-06   | 7.56e+00   | 8.25e-03   | 1.28e-02   |
| (20, 20, 0.5)               | 3.68e-04   | 9.06e-06   | 7.13e-01   | 1.21e-02   | 1.04e-01   |
| (20, 20, 0.6)               | 1.36e-04   | 6.44e-06   | 3.36e-02   | 5.23e-01   | 9.86e-01   |
| (20, 50, 0.3)               | 1.81e-01   | 3.72e-01   | nan        | 2.57e-02   | 3.78e+00   |
| (20, 50, 0.35)              | 2.03e-02   | 2.76e-02   | nan        | 2.36e-02   | 9.85e+00   |
| (20, 100, 0.2)              | 9.73e-02   | 4.33e+02   | nan        | 1.41e-01   | 6.70e+01   |
| (20, 100, 0.25)             | 1.91e-02   | 1.05e+00   | nan        | 9.13e-02   | 1.55e+02   |
| (50, 10, 0.83)              | 7.41e+00   | 3.43e-03   | nan        | nan        | 3.21e+02   |
| (50, 10, 0.85)              | 2.06e-02   | 5.82e-04   | nan        | 1.96e+02   | 5.66e+02   |
| (50, 20, 0.5)               | 2.00e-01   | 2.96e-02   | nan        | nan        | nan        |
| (50, 20, 0.6)               | 2.76e+00   | 4.69e-01   | nan        | nan        | nan        |
| (50, 20, 0.7)               | 1.63e+02   | 9.19e+01   | nan        | nan        | nan        |
| (50, 20, 0.71)              | 3.22e+02   | 1.13e+02   | nan        | nan        | nan        |
| (50, 20, 0.72)              | nan        | 3.73e+02   | nan        | nan        | nan        |
| (50, 20, 0.73)              | nan        | 8.87e+02   | nan        | nan        | nan        |
| (50, 20, 0.75)              | nan        | nan        | nan        | nan        | nan        |
| (50, 20, 0.76)              | nan        | nan        | nan        | nan        | nan        |
| (50, 20, 0.77)              | nan        | 3.96e+00   | nan        | nan        | nan        |
| (50, 20, 0.78)              | nan        | 3.34e+00   | nan        | nan        | nan        |
| (50, 20, 0.79)              | nan        | 7.76e-02   | nan        | nan        | nan        |
| (50, 20, 0.8)               | nan        | 8.61e-04   | nan        | nan        | nan        |
| (50, 50, 0.1)               | 3.74e-02   | 5.94e+00   | nan        | nan        | nan        |
| (50, 50, 0.2)               | 9.52e-02   | 1.41e+01   | nan        | nan        | nan        |
| (50, 50, 0.3)               | 1.90e+00   | 2.59e+02   | nan        | nan        | nan        |
| (50, 50, 0.4)               | 2.08e+01   | nan        | nan        | nan        | nan        |
| (50, 50, 0.5)               | 8.57e+02   | nan        | nan        | nan        | nan        |
| (50, 50, 0.6)               | nan        | nan        | nan        | nan        | nan        |
| (50, 50, 0.71)              | nan        | nan        | nan        | nan        | nan        |
| (50, 50, 0.72)              | nan        | 1.58e+01   | nan        | nan        | nan        |
| (50, 50, 0.73)              | nan        | 1.39e+01   | nan        | nan        | nan        |
| (50, 50, 0.74)              | nan        | 3.01e-01   | nan        | 1.48e+02   | nan        |
| (50, 100, 0.1)              | 2.30e-01   | nan        | nan        | nan        | nan        |
| (50, 100, 0.2)              | 1.04e+01   | nan        | nan        | nan        | nan        |
| (50, 100, 0.3)              | 2.24e+02   | nan        | nan        | nan        | nan        |
| (50, 100, 0.4)              | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.64)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.65)             | nan        | nan        | nan        | 6.39e+01   | nan        |
| (50, 100, 0.66)             | nan        | nan        | nan        | 3.29e+01   | nan        |
| (50, 100, 0.67)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.68)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.69)             | nan        | 1.84e+02   | nan        | 7.86e-01   | nan        |
| (50, 100, 0.7)              | nan        | 1.68e+01   | nan        | nan        | nan        |
| (100, 10, 0.6)              | 3.85e-03   | 1.26e-05   | nan        | nan        | nan        |
| (100, 10, 0.7)              | 1.33e-02   | 1.86e-05   | nan        | nan        | nan        |
| (100, 10, 0.8)              | 5.41e-01   | 3.49e-03   | nan        | nan        | nan        |
| (100, 20, 0.4)              | 4.76e-02   | 1.55e-03   | nan        | nan        | nan        |
| (100, 20, 0.5)              | 4.99e-01   | 6.19e-03   | nan        | nan        | nan        |
| (100, 20, 0.6)              | 4.35e+00   | 1.30e-01   | nan        | nan        | nan        |
| (100, 20, 0.7)              | 4.42e+02   | 2.91e+00   | nan        | nan        | nan        |
| (100, 20, 0.8)              | nan        | nan        | nan        | nan        | nan        |
| (100, 20, 0.89)             | nan        | nan        | nan        | nan        | nan        |
| (100, 20, 0.9)              | nan        | 1.69e+00   | nan        | nan        | nan        |
| (100, 50, 0.1)              | 1.59e-01   | 1.20e+01   | nan        | nan        | nan        |
| (100, 50, 0.2)              | 2.77e-01   | 3.54e+01   | nan        | nan        | nan        |
| (100, 50, 0.3)              | 8.45e+00   | 5.05e+02   | nan        | nan        | nan        |
| (100, 50, 0.4)              | 3.99e+01   | nan        | nan        | nan        | nan        |
| (100, 50, 0.5)              | nan        | nan        | nan        | nan        | nan        |
| (100, 50, 0.87)             | nan        | nan        | nan        | nan        | nan        |
| (100, 50, 0.88)             | nan        | 2.64e+00   | nan        | nan        | nan        |
| (100, 50, 0.89)             | nan        | 1.58e-02   | nan        | nan        | nan        |
| (100, 50, 0.9)              | nan        | 2.91e-04   | nan        | nan        | nan        |
| (100, 100, 0.1)             | 9.02e-01   | nan        | nan        | nan        | nan        |
| (100, 100, 0.2)             | 4.12e+01   | nan        | nan        | nan        | nan        |
| (100, 100, 0.3)             | 2.63e+02   | nan        | nan        | nan        | nan        |
| (100, 100, 0.4)             | nan        | nan        | nan        | nan        | nan        |
| (100, 100, 0.85)            | nan        | nan        | nan        | nan        | nan        |
| (100, 100, 0.86)            | nan        | 1.51e+01   | nan        | nan        | nan        |
| (100, 100, 0.87)            | nan        | 3.93e-01   | nan        | nan        | nan        |
| (100, 100, 0.88)            | nan        | 9.61e-05   | nan        | nan        | nan        |
| (100, 100, 0.89)            | nan        | 9.18e-05   | nan        | nan        | nan        |
| (100, 100, 0.9)             | nan        | 8.42e-05   | nan        | nan        | nan        |

### Finding all k-cliques

We time how long it takes to find all k-clique,
if this time differs from above.

| Graph                       | kpkc       | FindClique | networkx   |
  ---                         | ---        | ---        | ---
| (5, 50, 50, 0.14, 0.14)     | 6.62e-04   | 3.22e-05   | 1.10e-02   |
| (5, 50, 50, 0.2, 0.2)       | 9.15e-04   | 1.10e-04   | 2.32e-02   |
| (5, 50, 50, 0.25, 0.25)     | 2.36e-03   | 6.10e-04   | 4.27e-02   |
| (5, 50, 50, 0.0, 0.3)       | 7.50e-04   | 5.13e-05   | 1.45e-02   |
| (5, 50, 50, 0.0, 0.4)       | 1.53e-03   | 3.56e-04   | 2.87e-02   |
| (5, 50, 50, 0.0, 0.45)      | 2.65e-03   | 9.86e-04   | 3.81e-02   |
| (5, 50, 50, 0.0, 0.5)       | 5.42e-03   | 2.67e-03   | 5.24e-02   |
| (10, 26, 37, 0.49, 0.49)    | 3.13e-02   | 5.78e-04   | 1.68e+01   |
| (10, 26, 37, 0.5, 0.5)      | 3.77e-02   | 6.79e-04   | 8.44e+00   |
| (10, 26, 37, 0.51, 0.51)    | 4.05e-02   | 7.99e-04   | 8.81e+00   |
| (10, 26, 37, 0.4, 0.6)      | 4.58e-02   | 9.74e-04   | 1.07e+01   |
| (10, 26, 37, 0.3, 0.7)      | 6.86e-02   | 3.56e-03   | 1.36e+01   |
| (10, 50, 50, 0.43, 0.43)    | 1.15e-01   | 1.95e-03   | 2.53e+01   |
| (10, 50, 50, 0.44, 0.44)    | 1.56e-01   | 2.56e-03   | 3.36e+01   |
| (10, 50, 50, 0.46, 0.46)    | 3.08e-01   | 4.57e-03   | 5.33e+01   |
| (10, 50, 50, 0.48, 0.48)    | 6.14e-01   | 8.58e-03   | 8.61e+01   |
| (10, 50, 50, 0.5, 0.5)      | 1.08e+00   | 2.22e-02   | 1.42e+02   |
| (50, 5, 15, 0.918, 0.918)   | nan        | 1.89e+00   | nan        |
| (50, 5, 15, 0.92, 0.92)     | nan        | 4.94e+01   | nan        |
| (20, 23, 39, 0.71, 0.71)    | 5.19e+02   | 3.48e-01   | nan        |
| (20, 23, 39, 0.72, 0.72)    | nan        | 1.12e+00   | nan        |
| (20, 23, 39, 0.7, 0.73)     | 7.80e+02   | 5.32e-01   | nan        |
| (20, 23, 39, 0.65, 0.78)    | 6.64e+02   | 5.31e-01   | nan        |
| (30, 11, 30, 0.82, 0.82)    | nan        | 8.82e-01   | nan        |
| (30, 11, 30, 0.84, 0.84)    | nan        | 7.01e+01   | nan        |
| (3, 100, 100, 0.1, 0.1)     | 2.81e-03   | 1.74e-03   | 6.62e-03   |
| (4, 100, 100, 0.15, 0.15)   | 5.01e-03   | 2.02e-03   | 3.99e-02   |
| (5, 100, 100, 0.2, 0.2)     | 1.25e-02   | 2.10e-03   | 1.85e-01   |
| (6, 100, 100, 0.25, 0.25)   | 4.08e-02   | 3.08e-03   | 1.01e+00   |
| (7, 50, 50, 0.35, 0.35)     | 1.64e-02   | 8.58e-04   | 7.00e-01   |
| (8, 50, 50, 0.4, 0.4)       | 4.57e-02   | 1.90e-03   | 3.63e+00   |
| (9, 50, 50, 0.45, 0.45)     | 1.91e-01   | 5.27e-03   | 2.10e+01   |
| (10, 50, 50, 0.5, 0.5)      | 1.04e+00   | 2.01e-02   | 1.39e+02   |
| (10, 10, 10, 0.74, 0.74)    | 6.61e-02   | 3.10e-02   | 1.16e+00   |
| (10, 22, 22, 0.65, 0.65)    | 4.99e-01   | 1.51e-01   | 2.84e+01   |
| (10, 48, 48, 0.59, 0.59)    | 2.57e+01   | 7.69e+00   | nan        |
| (5, 10, 0.1)                | 1.10e-04   | 7.30e-05   | 4.87e-04   |
| (5, 10, 0.2)                | 1.94e-04   | 1.41e-04   | 5.51e-04   |
| (5, 20, 0.05)               | 2.93e-03   | 2.30e-03   | 5.23e-03   |
| (5, 20, 0.1)                | 3.85e-03   | 3.09e-03   | 6.47e-03   |
| (5, 50, 0.01)               | 7.54e-02   | 6.29e-02   | 1.36e-01   |
| (5, 50, 0.02)               | 1.09e-01   | 9.27e-02   | 1.66e-01   |
| (10, 10, 0.4)               | 4.80e-04   | 1.70e-04   | 1.77e-02   |
| (10, 10, 0.6)               | 2.44e-02   | 1.34e-02   | 5.13e-02   |
| (10, 20, 0.3)               | 3.35e-02   | 1.85e-02   | 8.44e-01   |
| (10, 20, 0.5)               | 2.29e+00   | 1.65e+00   | 4.88e+00   |
| (10, 50, 0.05)              | 5.68e-02   | 6.52e-02   | 3.01e+01   |
| (10, 50, 0.1)               | 2.59e-01   | 2.04e-01   | 4.62e+01   |
| (10, 100, 0.01)             | 5.24e+00   | 7.33e+00   | nan        |
| (10, 100, 0.02)             | 9.22e+00   | 1.13e+01   | nan        |
| (20, 10, 0.6)               | 2.31e-03   | 1.86e-04   | 1.59e+01   |
| (20, 10, 0.7)               | 9.11e-01   | 3.48e-01   | 9.67e+01   |
| (20, 20, 0.5)               | 1.31e-01   | 8.80e-02   | nan        |
| (20, 20, 0.6)               | 3.49e+01   | 2.21e+01   | nan        |
| (20, 50, 0.3)               | 1.11e+00   | 2.40e+01   | nan        |
| (20, 50, 0.35)              | 4.40e+00   | 7.32e+01   | nan        |
| (20, 100, 0.2)              | 8.36e+00   | nan        | nan        |
| (20, 100, 0.25)             | 4.31e+01   | nan        | nan        |
| (50, 10, 0.83)              | 2.24e+01   | 4.36e-01   | nan        |
| (50, 10, 0.85)              | nan        | 6.89e+01   | nan        |

### Conclusion

According to the above timings,
`kpkc` and `FindClique` appear to be best choices for finding k-cliques in k-partite graphs.
- If all vertices are expected to have somewhat the same number of neighbors,
  then `FindClique` is the best choice.
- If there are many edges and the expected number of k-cliques is large,
  then `FindClique` is the best choice to obtain
  some k-cliques.
- If only few k-cliques (if any) are exepcted and
  vertices in larger parts have fewer neighbors
  than vertices in smaller parts, then `kpkc` is
  the best choice to obtain all k-cliques.

Note that our implementation of `FindClique` appears to be faster
in finding all k-cliques than the original implementations (which are
not published) in

- Grunert, Tore & Irnich, Stefan & Zimmermann, Hans-Jürgen & Schneider, Markus & Wulfhorst, Burkhard. (2001). Cliques in k-partite Graphs and their Application in Textile Engineering

and

- Mirghorbani, M. & Krokhmal, P.. (2013). On finding k-cliques in k-partite graphs. Optimization Letters. 7. 10.1007/s11590-012-0536-y

It is significantly faster in finding the first k-clique:
All cases with random graphs from the above two papers could be handled in less than a
second, with three exceptions:
- `(100, 10, 10, 0.92, 0.92)`, which takes 5 seconds now, instead of
  4000 seconds originally by Grunert et. al.,
- `(100, 10, 10, 0,94, 0.94)` remains infeasible in the given time,
- `(100, 10, 10, 0,95, 0.95)` remains infeasible in the given time.
The original implementation of `FindClique` by Grundert et. al. apparently needed more than 100
seconds for random graphs with several different parameters to find the
first k-clique.

The paper by Mirghorbani and Krokhmal lists several new parameters to
time obtaining the first k-clique. We could not reproduce timings above
one tenth of a millisecond, even in those cases that apparently took 10, 50 and 250
seconds respectively.
