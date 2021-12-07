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

  - Grünert, Tore & Irnich, Stefan & Zimmermann, Hans-Jürgen & Schneider, Markus & Wulfhorst, Burkhard. (2001). Cliques in k-partite Graphs and their Application in Textile Engineering

  Such a random graph can be obtain with
  `kpkc.test.get_random_k_partite_graph(k, min_s, max_s, a_1, a_2)`.
- In addition we benchmark examples with parameters `(k, max_s, a)`,
  where `k` is the number of parts.
  Parts have sizes `1 + ((max_s -1) * i) // k` for `i` in 1, ..., k.

  Let `f` be the affine function determined by `f(1) = 1` and `f(max_s) =
  a`.
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
| 0                           | 1.73e+01   | nan        | nan        | nan        | nan        |
| 1                           | 1.73e+01   | nan        | nan        | nan        | nan        |
| 2                           | 1.72e+01   | nan        | nan        | nan        | nan        |
| 20                          | 5.07e+00   | nan        | nan        | nan        | nan        |
| 100                         | 1.74e+01   | nan        | nan        | nan        | nan        |
| 1000                        | 4.89e-01   | 2.15e+01   | nan        | nan        | nan        |
| 10000                       | 1.78e-01   | 3.62e+00   | nan        | 6.26e+02   | nan        |
| 1000000                     | 1.32e+00   | nan        | nan        | nan        | nan        |
| 2000000                     | 1.58e-01   | 7.63e-01   | nan        | 9.44e+00   | nan        |
| 5000000                     | 1.87e-01   | 7.95e+00   | nan        | nan        | nan        |
| 10000000                    | 2.25e-02   | 6.11e-03   | nan        | 1.24e+00   | nan        |
| (5, 50, 50, 0.14, 0.14)     | 5.61e-04   | 2.31e-05   | 1.08e-02   | 1.28e-03   | 1.20e-03   |
| (5, 50, 50, 0.15, 0.15)     | 2.78e-04   | 2.00e-05   | 3.57e-03   | 1.39e-03   | 1.27e-03   |
| (5, 50, 50, 0.2, 0.2)       | 4.17e-05   | 5.01e-06   | 1.77e-03   | 1.67e-03   | 1.60e-03   |
| (5, 50, 50, 0.25, 0.25)     | 5.44e-05   | 3.34e-06   | 1.36e-03   | 2.21e-03   | 2.06e-03   |
| (5, 50, 50, 0.0, 0.3)       | 1.93e-04   | 4.77e-06   | 1.22e-03   | 1.27e-03   | 1.26e-03   |
| (5, 50, 50, 0.0, 0.4)       | 3.12e-05   | 3.34e-06   | 1.15e-03   | 1.57e-03   | 1.58e-03   |
| (5, 50, 50, 0.0, 0.45)      | 1.00e-05   | 3.34e-06   | 1.34e-03   | 2.13e-03   | 1.97e-03   |
| (5, 50, 50, 0.0, 0.5)       | 1.22e-05   | 3.34e-06   | 1.42e-03   | 2.12e-03   | 2.00e-03   |
| (10, 26, 37, 0.49, 0.49)    | 3.48e-03   | 5.84e-05   | 2.59e-01   | 4.55e-02   | 4.47e-02   |
| (10, 26, 37, 0.5, 0.5)      | 9.58e-05   | 5.25e-06   | 3.51e-02   | 5.70e-02   | 3.83e-02   |
| (10, 26, 37, 0.51, 0.51)    | 1.39e-03   | 1.14e-05   | 7.50e-01   | 1.10e-01   | 6.55e-02   |
| (10, 26, 37, 0.4, 0.6)      | 1.88e-03   | 5.96e-06   | 2.17e-01   | 7.19e-02   | 4.76e-02   |
| (10, 26, 37, 0.3, 0.7)      | 6.03e-04   | 1.03e-05   | 1.28e-02   | 1.52e-01   | 5.06e-02   |
| (10, 50, 50, 0.42, 0.42)    | 1.33e-02   | 2.52e-04   | 1.09e+00   | 1.07e-01   | 1.13e-01   |
| (10, 50, 50, 0.43, 0.43)    | 4.42e-03   | 1.56e-04   | 1.70e+00   | 1.80e-01   | 1.31e-01   |
| (10, 50, 50, 0.44, 0.44)    | 2.25e-02   | 8.18e-05   | 3.16e-01   | 2.14e-01   | 1.70e-01   |
| (10, 50, 50, 0.46, 0.46)    | 5.23e-03   | 2.17e-05   | 2.67e-02   | 3.24e-01   | 2.75e-01   |
| (10, 50, 50, 0.48, 0.48)    | 9.79e-04   | 3.22e-05   | 4.92e-02   | 4.04e-01   | 3.95e-01   |
| (10, 50, 50, 0.5, 0.5)      | 7.41e-04   | 9.78e-06   | 1.58e-02   | 1.16e+00   | 6.94e-01   |
| (50, 5, 15, 0.91, 0.91)     | nan        | 6.35e-02   | nan        | nan        | nan        |
| (50, 5, 15, 0.918, 0.918)   | nan        | 2.81e-02   | nan        | nan        | nan        |
| (50, 5, 15, 0.92, 0.92)     | nan        | 7.89e-03   | nan        | nan        | nan        |
| (20, 23, 39, 0.7, 0.7)      | 1.87e+02   | 1.06e-01   | nan        | nan        | nan        |
| (20, 23, 39, 0.71, 0.71)    | 4.07e+01   | 5.18e-02   | nan        | nan        | nan        |
| (20, 23, 39, 0.72, 0.72)    | 5.12e+00   | 1.81e-03   | nan        | nan        | nan        |
| (20, 23, 39, 0.7, 0.73)     | 2.57e+00   | 3.55e-03   | nan        | nan        | nan        |
| (20, 23, 39, 0.65, 0.78)    | 1.04e+00   | 7.39e-05   | nan        | nan        | nan        |
| (30, 11, 30, 0.6, 0.6)      | 4.29e-01   | 1.29e-04   | nan        | 7.96e+02   | 1.21e+02   |
| (30, 11, 30, 0.7, 0.7)      | 1.63e+01   | 1.40e-03   | nan        | nan        | nan        |
| (30, 11, 30, 0.8, 0.8)      | nan        | 1.16e+00   | nan        | nan        | nan        |
| (30, 11, 30, 0.81, 0.81)    | nan        | 1.33e+00   | nan        | nan        | nan        |
| (30, 11, 30, 0.82, 0.82)    | nan        | 4.36e-01   | nan        | nan        | nan        |
| (30, 11, 30, 0.84, 0.84)    | nan        | 5.73e-03   | nan        | nan        | nan        |
| (30, 11, 30, 0.88, 0.88)    | 1.44e+00   | 1.22e-05   | nan        | nan        | nan        |
| (100, 10, 10, 0.7, 0.7)     | 5.20e-02   | 4.67e-05   | nan        | nan        | nan        |
| (100, 10, 10, 0.8, 0.8)     | 4.76e+00   | 3.47e-04   | nan        | nan        | nan        |
| (100, 10, 10, 0.85, 0.85)   | 2.21e+02   | 1.94e-03   | nan        | nan        | nan        |
| (100, 10, 10, 0.9, 0.9)     | nan        | 1.49e-01   | nan        | nan        | nan        |
| (100, 10, 10, 0.92, 0.92)   | nan        | 4.19e+00   | nan        | nan        | nan        |
| (100, 10, 10, 0.94, 0.94)   | nan        | nan        | nan        | nan        | nan        |
| (100, 10, 10, 0.95, 0.95)   | nan        | nan        | nan        | nan        | nan        |
| (100, 10, 10, 0.97, 0.97)   | nan        | 2.61e-03   | nan        | nan        | nan        |
| (3, 100, 100, 0.1, 0.1)     | 1.00e-05   | 2.62e-06   | 9.16e-04   | 1.29e-03   | 1.20e-03   |
| (4, 100, 100, 0.15, 0.15)   | 1.45e-05   | 3.81e-06   | 2.01e-03   | 3.61e-03   | 3.47e-03   |
| (5, 100, 100, 0.2, 0.2)     | 3.41e-05   | 3.34e-06   | 4.94e-03   | 8.59e-03   | 8.80e-03   |
| (6, 100, 100, 0.25, 0.25)   | 1.02e-04   | 6.44e-06   | 8.21e-03   | 2.33e-02   | 2.31e-02   |
| (7, 50, 50, 0.35, 0.35)     | 3.46e-05   | 6.91e-06   | 7.86e-03   | 1.26e-02   | 1.15e-02   |
| (8, 50, 50, 0.4, 0.4)       | 1.40e-04   | 6.68e-06   | 1.17e-02   | 3.85e-02   | 3.41e-02   |
| (9, 50, 50, 0.45, 0.45)     | 1.50e-04   | 5.98e-05   | 8.81e-03   | 1.71e-01   | 1.25e-01   |
| (10, 50, 50, 0.5, 0.5)      | 8.56e-04   | 1.24e-05   | 1.43e-01   | 1.48e+00   | 6.43e-01   |
| (5, 10, 0.1)                | 6.91e-06   | 2.86e-06   | 1.08e-04   | 8.94e-05   | 1.07e-04   |
| (5, 10, 0.2)                | 5.48e-06   | 2.62e-06   | 9.66e-05   | 7.39e-05   | 9.49e-05   |
| (5, 20, 0.05)               | 6.91e-06   | 2.86e-06   | 2.21e-04   | 2.05e-04   | 2.45e-04   |
| (5, 20, 0.1)                | 6.44e-06   | 2.86e-06   | 2.56e-04   | 2.08e-04   | 2.54e-04   |
| (5, 50, 0.01)               | 1.22e-05   | 3.10e-06   | 9.59e-04   | 1.09e-03   | 1.17e-03   |
| (5, 50, 0.02)               | 1.10e-05   | 3.10e-06   | 9.73e-04   | 1.06e-03   | 1.20e-03   |
| (10, 10, 0.4)               | 1.19e-05   | 3.34e-06   | 4.68e-04   | 2.12e-04   | 2.93e-04   |
| (10, 10, 0.6)               | 1.53e-05   | 3.58e-06   | 3.96e-04   | 3.01e-04   | 3.04e-04   |
| (10, 20, 0.3)               | 2.00e-05   | 4.29e-06   | 2.03e-03   | 8.79e-04   | 1.06e-03   |
| (10, 20, 0.5)               | 2.31e-05   | 3.81e-06   | 1.33e-03   | 8.62e-04   | 3.01e-03   |
| (10, 50, 0.05)              | 4.84e-05   | 3.81e-06   | 1.91e-02   | 3.87e-03   | 4.93e-03   |
| (10, 50, 0.1)               | 6.82e-05   | 7.15e-06   | 4.94e-03   | 4.09e-03   | 5.39e-03   |
| (10, 100, 0.01)             | 6.79e-05   | 1.12e-05   | 1.90e-02   | 1.74e-02   | 7.28e-02   |
| (10, 100, 0.02)             | 7.37e-05   | 5.25e-06   | 1.35e-02   | 1.78e-02   | 7.60e-02   |
| (20, 10, 0.6)               | 2.16e-04   | 8.54e-05   | 1.62e+00   | 3.42e-03   | 2.46e-03   |
| (20, 10, 0.7)               | 6.68e-05   | 5.48e-06   | 4.99e-01   | 1.90e-02   | 8.59e-03   |
| (20, 20, 0.5)               | 6.92e-04   | 5.39e-05   | 6.10e+00   | 3.48e-03   | 6.79e-02   |
| (20, 20, 0.6)               | 1.01e-04   | 7.63e-06   | 1.37e-02   | 3.11e-03   | 9.25e-01   |
| (20, 50, 0.3)               | 8.63e-01   | 1.55e+01   | nan        | 4.66e-02   | 8.06e+00   |
| (20, 50, 0.35)              | 2.53e-02   | 3.24e-02   | nan        | 2.27e-02   | 9.18e+00   |
| (20, 100, 0.2)              | 1.40e-01   | 1.40e+02   | nan        | 1.21e-01   | 6.80e+01   |
| (20, 100, 0.25)             | 1.03e-01   | 8.80e-01   | nan        | 8.89e-02   | 5.48e+02   |
| (50, 10, 0.83)              | 1.04e+00   | 2.67e-03   | nan        | 1.36e+02   | 2.13e+02   |
| (50, 10, 0.85)              | 2.09e-01   | 2.95e-03   | nan        | nan        | 9.45e+02   |
| (50, 20, 0.5)               | 2.08e-01   | 2.00e-02   | nan        | nan        | nan        |
| (50, 20, 0.6)               | 2.52e+00   | 4.22e-01   | nan        | nan        | nan        |
| (50, 20, 0.7)               | 1.58e+02   | 2.38e+01   | nan        | nan        | nan        |
| (50, 20, 0.71)              | 3.04e+02   | 2.48e+02   | nan        | nan        | nan        |
| (50, 20, 0.72)              | nan        | 7.12e+02   | nan        | nan        | nan        |
| (50, 20, 0.73)              | nan        | 7.61e+02   | nan        | nan        | nan        |
| (50, 20, 0.75)              | nan        | nan        | nan        | nan        | nan        |
| (50, 20, 0.76)              | nan        | nan        | nan        | nan        | nan        |
| (50, 20, 0.77)              | nan        | 1.56e+01   | nan        | nan        | nan        |
| (50, 20, 0.78)              | nan        | 1.50e+00   | nan        | nan        | nan        |
| (50, 20, 0.79)              | nan        | 1.89e-01   | nan        | nan        | nan        |
| (50, 20, 0.8)               | nan        | 6.43e-03   | nan        | nan        | nan        |
| (50, 50, 0.1)               | 3.63e-02   | 4.46e+00   | nan        | nan        | nan        |
| (50, 50, 0.2)               | 1.28e-01   | 3.33e+01   | nan        | nan        | nan        |
| (50, 50, 0.3)               | 2.09e+00   | 1.74e+02   | nan        | nan        | nan        |
| (50, 50, 0.4)               | 2.46e+01   | nan        | nan        | nan        | nan        |
| (50, 50, 0.5)               | 8.03e+02   | nan        | nan        | nan        | nan        |
| (50, 50, 0.6)               | nan        | nan        | nan        | nan        | nan        |
| (50, 50, 0.71)              | nan        | nan        | nan        | nan        | nan        |
| (50, 50, 0.72)              | nan        | 2.99e+01   | nan        | 1.83e+02   | nan        |
| (50, 50, 0.73)              | nan        | 1.17e+01   | nan        | nan        | nan        |
| (50, 50, 0.74)              | nan        | 1.55e+00   | nan        | nan        | nan        |
| (50, 100, 0.1)              | 2.43e-01   | nan        | nan        | nan        | nan        |
| (50, 100, 0.2)              | 1.11e+01   | nan        | nan        | nan        | nan        |
| (50, 100, 0.3)              | 2.35e+02   | nan        | nan        | nan        | nan        |
| (50, 100, 0.4)              | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.64)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.65)             | nan        | nan        | nan        | 1.19e+02   | nan        |
| (50, 100, 0.66)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.67)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.68)             | nan        | nan        | nan        | nan        | nan        |
| (50, 100, 0.69)             | nan        | 2.28e+01   | nan        | nan        | nan        |
| (50, 100, 0.7)              | nan        | 2.27e+00   | nan        | 4.29e+01   | nan        |
| (100, 10, 0.6)              | 6.79e-03   | 9.54e-06   | nan        | nan        | nan        |
| (100, 10, 0.7)              | 2.35e-02   | 4.43e-05   | nan        | nan        | nan        |
| (100, 10, 0.8)              | 6.69e-01   | 1.71e-03   | nan        | nan        | nan        |
| (100, 20, 0.4)              | 4.81e-02   | 1.65e-03   | nan        | nan        | nan        |
| (100, 20, 0.5)              | 4.35e-01   | 1.33e-02   | nan        | nan        | nan        |
| (100, 20, 0.6)              | 4.65e+00   | 9.83e-02   | nan        | nan        | nan        |
| (100, 20, 0.7)              | 4.75e+02   | 9.96e+00   | nan        | nan        | nan        |
| (100, 20, 0.8)              | nan        | nan        | nan        | nan        | nan        |
| (100, 20, 0.89)             | nan        | nan        | nan        | nan        | nan        |
| (100, 20, 0.9)              | nan        | 2.43e+00   | nan        | nan        | nan        |
| (100, 50, 0.1)              | 1.78e-01   | 7.15e+00   | nan        | nan        | nan        |
| (100, 50, 0.2)              | 2.92e-01   | 8.19e+01   | nan        | nan        | nan        |
| (100, 50, 0.3)              | 8.12e+00   | 4.96e+02   | nan        | nan        | nan        |
| (100, 50, 0.4)              | 4.61e+01   | nan        | nan        | nan        | nan        |
| (100, 50, 0.5)              | nan        | nan        | nan        | nan        | nan        |
| (100, 50, 0.87)             | nan        | nan        | nan        | nan        | nan        |
| (100, 50, 0.88)             | nan        | 4.24e+00   | nan        | nan        | nan        |
| (100, 50, 0.89)             | nan        | 1.85e-03   | nan        | nan        | nan        |
| (100, 50, 0.9)              | nan        | 2.31e-04   | nan        | nan        | nan        |
| (100, 100, 0.1)             | 8.92e-01   | nan        | nan        | nan        | nan        |
| (100, 100, 0.2)             | 4.16e+01   | nan        | nan        | nan        | nan        |
| (100, 100, 0.3)             | 2.60e+02   | nan        | nan        | nan        | nan        |
| (100, 100, 0.4)             | nan        | nan        | nan        | nan        | nan        |
| (100, 100, 0.85)            | nan        | nan        | nan        | nan        | nan        |
| (100, 100, 0.86)            | nan        | 7.75e+00   | nan        | nan        | nan        |
| (100, 100, 0.87)            | nan        | 3.72e-03   | nan        | nan        | nan        |
| (100, 100, 0.88)            | nan        | 9.73e-05   | nan        | nan        | nan        |
| (100, 100, 0.89)            | nan        | 9.06e-05   | nan        | nan        | nan        |
| (100, 100, 0.9)             | nan        | 7.77e-05   | nan        | nan        | nan        |

### Finding all k-cliques

We time how long it takes to find all k-clique,
if this time differs from above.

| Graph                       | kpkc       | FindClique | networkx   |
  ---                         | ---        | ---        | ---
| (5, 50, 50, 0.15, 0.15)     | 5.86e-04   | 3.34e-05   | 1.27e-02   |
| (5, 50, 50, 0.2, 0.2)       | 8.09e-04   | 1.06e-04   | 2.39e-02   |
| (5, 50, 50, 0.25, 0.25)     | 2.29e-03   | 6.21e-04   | 4.34e-02   |
| (5, 50, 50, 0.0, 0.3)       | 6.28e-04   | 5.96e-05   | 1.33e-02   |
| (5, 50, 50, 0.0, 0.4)       | 1.09e-03   | 2.58e-04   | 2.48e-02   |
| (5, 50, 50, 0.0, 0.45)      | 3.20e-03   | 1.32e-03   | 4.34e-02   |
| (5, 50, 50, 0.0, 0.5)       | 4.15e-03   | 2.01e-03   | 4.48e-02   |
| (10, 26, 37, 0.49, 0.49)    | 4.04e-02   | 8.25e-04   | 9.43e+00   |
| (10, 26, 37, 0.5, 0.5)      | 3.48e-02   | 7.26e-04   | 8.26e+00   |
| (10, 26, 37, 0.51, 0.51)    | 6.90e-02   | 1.17e-03   | 1.42e+01   |
| (10, 26, 37, 0.4, 0.6)      | 4.68e-02   | 9.55e-04   | 1.39e+01   |
| (10, 26, 37, 0.3, 0.7)      | 6.58e-02   | 4.12e-03   | 1.27e+01   |
| (10, 50, 50, 0.42, 0.42)    | 9.31e-02   | 1.38e-03   | 2.14e+01   |
| (10, 50, 50, 0.43, 0.43)    | 1.21e-01   | 1.94e-03   | 2.78e+01   |
| (10, 50, 50, 0.44, 0.44)    | 1.51e-01   | 2.48e-03   | 3.46e+01   |
| (10, 50, 50, 0.46, 0.46)    | 3.04e-01   | 4.25e-03   | 5.52e+01   |
| (10, 50, 50, 0.48, 0.48)    | 5.73e-01   | 7.96e-03   | 8.39e+01   |
| (10, 50, 50, 0.5, 0.5)      | 9.97e-01   | 1.97e-02   | 1.72e+02   |
| (50, 5, 15, 0.918, 0.918)   | nan        | 1.06e+01   | nan        |
| (50, 5, 15, 0.92, 0.92)     | nan        | 2.91e+00   | nan        |
| (20, 23, 39, 0.7, 0.7)      | 3.20e+02   | 1.93e-01   | nan        |
| (20, 23, 39, 0.71, 0.71)    | 5.35e+02   | 3.45e-01   | nan        |
| (20, 23, 39, 0.72, 0.72)    | 9.55e+02   | 6.42e-01   | nan        |
| (20, 23, 39, 0.7, 0.73)     | nan        | 8.67e-01   | nan        |
| (20, 23, 39, 0.65, 0.78)    | 4.54e+02   | 4.36e-01   | nan        |
| (30, 11, 30, 0.82, 0.82)    | nan        | 3.45e+00   | nan        |
| (30, 11, 30, 0.84, 0.84)    | nan        | 5.13e+01   | nan        |
| (3, 100, 100, 0.1, 0.1)     | 2.57e-03   | 1.64e-03   | 6.51e-03   |
| (4, 100, 100, 0.15, 0.15)   | 4.71e-03   | 2.08e-03   | 4.01e-02   |
| (5, 100, 100, 0.2, 0.2)     | 1.17e-02   | 2.23e-03   | 1.90e-01   |
| (6, 100, 100, 0.25, 0.25)   | 3.56e-02   | 2.80e-03   | 9.96e-01   |
| (7, 50, 50, 0.35, 0.35)     | 1.56e-02   | 8.15e-04   | 7.38e-01   |
| (8, 50, 50, 0.4, 0.4)       | 4.42e-02   | 1.91e-03   | 3.89e+00   |
| (9, 50, 50, 0.45, 0.45)     | 1.74e-01   | 4.50e-03   | 2.05e+01   |
| (10, 50, 50, 0.5, 0.5)      | 9.25e-01   | 1.67e-02   | 1.31e+02   |
| (5, 10, 0.1)                | 8.42e-05   | 5.44e-05   | 4.51e-04   |
| (5, 10, 0.2)                | 1.61e-04   | 1.08e-04   | 5.16e-04   |
| (5, 20, 0.05)               | 1.26e-03   | 9.48e-04   | 3.76e-03   |
| (5, 20, 0.1)                | 3.38e-03   | 2.70e-03   | 6.13e-03   |
| (5, 50, 0.01)               | 9.16e-02   | 7.71e-02   | 1.55e-01   |
| (5, 50, 0.02)               | 1.11e-01   | 9.42e-02   | 1.66e-01   |
| (10, 10, 0.4)               | 4.48e-03   | 1.99e-03   | 2.19e-02   |
| (10, 10, 0.6)               | 2.22e-02   | 1.15e-02   | 5.11e-02   |
| (10, 20, 0.3)               | 4.96e-02   | 2.72e-02   | 7.90e-01   |
| (10, 20, 0.5)               | 1.16e+00   | 7.80e-01   | 3.28e+00   |
| (10, 50, 0.05)              | 4.92e-02   | 6.55e-02   | 3.68e+01   |
| (10, 50, 0.1)               | 2.37e-01   | 1.89e-01   | 4.76e+01   |
| (10, 100, 0.01)             | 5.87e+00   | 7.79e+00   | nan        |
| (10, 100, 0.02)             | 8.49e+00   | 9.93e+00   | nan        |
| (20, 10, 0.6)               | 3.58e-03   | 8.23e-04   | 2.36e+01   |
| (20, 10, 0.7)               | 1.23e+00   | 4.68e-01   | 1.11e+02   |
| (20, 20, 0.5)               | 6.57e-02   | 4.46e-02   | nan        |
| (20, 20, 0.6)               | 2.82e+01   | 1.61e+01   | nan        |
| (20, 50, 0.35)              | 4.09e+00   | 6.97e+01   | nan        |
| (20, 100, 0.2)              | 9.58e+00   | nan        | nan        |
| (20, 100, 0.25)             | 4.70e+01   | nan        | nan        |
| (50, 10, 0.83)              | 1.30e+01   | 4.04e-01   | nan        |
| (50, 10, 0.85)              | nan        | 3.50e+01   | nan        |

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

- Grünert, Tore & Irnich, Stefan & Zimmermann, Hans-Jürgen & Schneider, Markus & Wulfhorst, Burkhard. (2001). Cliques in k-partite Graphs and their Application in Textile Engineering

and

- Mirghorbani, M. & Krokhmal, P.. (2013). On finding k-cliques in k-partite graphs. Optimization Letters. 7. 10.1007/s11590-012-0536-y

For random graphs with parameters `(k, min_s, max_s, a_1, a_2)`
and `k = 100` we improve the benchmarks of Grünert et. all by a factor
of 100. Note that we also use 3.6 GHz instead of 100 MHz leaving an
improvement factor of about 28.

Mirghorbani et. al. improved the implementation of `FindClique` by a
factor of up to `9` in comparison to Grünert et. al.
