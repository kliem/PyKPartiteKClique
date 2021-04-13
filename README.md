# PyKPartiteKClique

A python wrapper of https://github.com/kliem/KPartiteKClique.

# Requirements

- `setuptools`
- `Cython`

# Recommendations

- `cysignals` (allow keyboard interrupt)

# Benchmark

We benchmark implementations for the following graphs:

- Graphs in `sample_graphs/` that can be tested with
`kpkc.test.load_tester`.
- Also we benchmark random graphs with parameters `(k, min_s, max_s, a_1, a_2)`,
  where `k` is the number of parts,
  each part has size in `[min_s, max_s]` chosen with uniform distribution.
  Each vertex `v` is assigned a random float `p(v)` chosen with uniform
  distribution from `[a_1,a_2]`.
  For all pairs `v`, `w` from different parts the edge is generated with
  probability `(p(v) + p(w))/2`.

  This approach is described in:

  - Grunert, Tore & Irnich, Stefan & Zimmermann, Hans-Jürgen & Schneider, Markus & Wulfhorst, Burkhard. (2001). Cliques in k-partite Graphs and their Application in Textile Engineering

  Such a random graph can be obtain with
  `kpkc.test.get_random_k_partite_graph(k, min_s, max_s, a_1, a_2)`.
- In addition we benchmark examples with paramters `(k, max_s, a)`,
  where `k` is the number of parts.
  Parts have sizes `1 + ((max_s -1) * i) // k` for `i` in `1`, ..., `k`.

  Let `f` be the affine function determined by `f(1) = 1` and `f(a) =
  max_s`.
  For all pairs `v`, `w` from different parts with sizes `s`, `t`,
  the edge is generated with probability `f(min(s, t))`.

  This means parts of size `1` will have all neighbors and the more
  vertices a part has, the lower will be the density of its edges.

  Such a random graph can be obtain with
  `kpkc.test.get_random_k_partite_graph_2(k, max_s, a)`.

  In many contexts this might be a more natural choice than the above
  random graph. If the k-clique corresponds to some matching, than
  this corresponds to the fact that fewer choices means that people will
  be less picky. Example:

  Suppose there is only one cement mill in the area, two concrete
  pumps, twenty conrete mixer trucks, and a twenty concrete crews.
  Nobody can question the quality of the cement mill, because there is
  no alternative.
  As there is only two concrete pumps, the truck drivers will usually
  be willing to work with both of them.
  Likewise the concrete crews will usually put up with both pump
  operators.
  However, it is very much possible that the conrete crews might refuse
  to work with some truck drivers (always late) or the truck drivers
  might to refuse to work with some crews (always order more trucks than
  they need).

  In particular, the graphs in `sample_graphs/` behave somewhat like
  this. There are more than 14 million of those that we would like to
  check. This is feasible with `kpkc` and appears infeasible with the
  other implementations.

The results have been obtained with an Intel i7-7700 CPU @3.60GHz.

We use the following algorithms/implementations:

- `kpkc` (our implementation)
- `FindClique` (our implementation)
- `Cliquer` (exposed via `SageMath`)
- `networkx`
- `mcqd` (exposed via `SageMath`)

## Checking for a k-clique

We time how long it takes to either determine the clique number or to
find the first k-clique, if any.

Note that the graphs in `sample_graphs` do not have k-cliques.

Dashes indicate that the computation was interrupted after 1000s (without
determination).

| Graph                       | kpkc       | FindClique | networkx   | Cliquer    | mcqd     |
  ---                         | ---        | ---        | ---        | ---        | ---
| 0                           | 1.65e+01   | nan        | nan        | nan        | nan      |
| 1                           | 1.85e+01   | nan        | nan        | nan        | nan      |
| 2                           | 1.81e+01   | nan        | nan        | nan        | nan      |
| 20                          | 4.89e+00   | nan        | nan        | nan        | nan      |
| 100                         | 1.82e+01   | nan        | nan        | nan        | nan      |
| 1000                        | 2.45e-01   | 8.73e+00   | nan        | nan        | 1.54e+01 |
| 10000                       | 8.04e-02   | 3.92e+00   | nan        | nan        | 4.96e+00 |
| 1000000                     | 1.48e+00   | nan        | nan        | nan        | nan      |
| 2000000                     | 6.86e-02   | 9.17e-01   | nan        | 1.48e+01   | 3.86e+00 |
| 5000000                     | 1.66e-01   | 7.67e+00   | nan        | nan        | 1.58e+01 |
| 10000000                    | 1.77e-02   | 1.80e-04   | nan        | 1.32e+00   | 8.67e-01 |
| (5, 50, 50, 0.14, 0.14)     | 1.01e-03   | 4.05e-05   | 1.04e-02   | 1.37e-03   | 1.54e-03 |
| (5, 50, 50, 0.15, 0.15)     | 2.93e-04   | 1.57e-05   | 2.70e-03   | 1.40e-03   | 1.26e-03 |
| (5, 50, 50, 0.2, 0.2)       | 5.70e-05   | 6.68e-06   | 1.67e-03   | 1.73e-03   | 1.57e-03 |
| (5, 50, 50, 0.25, 0.25)     | 1.57e-05   | 5.48e-06   | 2.10e-03   | 2.21e-03   | 2.05e-03 |
| (5, 50, 50, 0.0, 0.3)       | 2.88e-04   | 5.01e-06   | 1.51e-03   | 1.43e-03   | 1.31e-03 |
| (5, 50, 50, 0.0, 0.4)       | 4.89e-05   | 5.72e-06   | 1.29e-03   | 1.91e-03   | 1.78e-03 |
| (5, 50, 50, 0.0, 0.45)      | 3.48e-05   | 3.34e-06   | 1.22e-03   | 2.14e-03   | 1.92e-03 |
| (5, 50, 50, 0.0, 0.5)       | 2.05e-05   | 3.58e-06   | 1.64e-03   | 2.19e-03   | 2.43e-03 |
| (10, 26, 37, 0.49, 0.49)    | 7.31e-03   | 3.26e-04   | 3.36e+00   | 4.54e-02   | 2.97e-02 |
| (10, 26, 37, 0.5, 0.5)      | 2.88e-04   | 1.81e-05   | 3.34e-02   | 6.47e-02   | 5.74e-02 |
| (10, 26, 37, 0.51, 0.51)    | 1.99e-03   | 4.15e-05   | 3.39e-01   | 7.53e-02   | 5.47e-02 |
| (10, 26, 37, 0.4, 0.6)      | 1.52e-03   | 2.65e-05   | 1.09e-01   | 6.45e-02   | 3.99e-02 |
| (10, 26, 37, 0.3, 0.7)      | 2.95e-04   | 1.29e-05   | 2.88e-02   | 1.43e-01   | 4.99e-02 |
| (10, 50, 50, 0.42, 0.42)    | 1.64e-02   | 2.42e-04   | 3.87e-01   | 2.14e-01   | 1.06e-01 |
| (10, 50, 50, 0.43, 0.43)    | 2.45e-02   | 4.41e-05   | 1.03e+00   | 1.36e-01   | 1.38e-01 |
| (10, 50, 50, 0.44, 0.44)    | 1.89e-02   | 6.91e-06   | 1.90e-01   | 1.93e-01   | 1.70e-01 |
| (10, 50, 50, 0.46, 0.46)    | 6.78e-04   | 1.62e-05   | 7.35e-02   | 2.93e-01   | 2.59e-01 |
| (10, 50, 50, 0.48, 0.48)    | 1.11e-02   | 1.22e-05   | 5.90e-02   | 5.79e-01   | 4.02e-01 |
| (10, 50, 50, 0.5, 0.5)      | 9.46e-04   | 9.78e-06   | 1.96e-01   | 1.93e+00   | 6.68e-01 |
| (10, 50, 50, 0.4, 0.6)      | 6.72e-04   | 8.82e-06   | 1.98e-02   | 2.46e+00   | 7.80e-01 |
| (10, 50, 50, 0.0, 0.8)      | 1.26e-04   | 7.63e-06   | 1.17e-02   | 1.44e+00   | 3.57e-01 |
| (50, 5, 15, 0.91, 0.91)     | nan        | 3.22e-02   | nan        | nan        | nan      |
| (50, 5, 15, 0.918, 0.918)   | nan        | 9.99e-02   | nan        | nan        | nan      |
| (50, 5, 15, 0.92, 0.92)     | nan        | 4.61e-03   | nan        | nan        | nan      |
| (20, 23, 39, 0.7, 0.7)      | 3.34e+02   | 2.47e-01   | nan        | nan        | nan      |
| (20, 23, 39, 0.71, 0.71)    | 6.36e+01   | 3.37e-02   | nan        | nan        | nan      |
| (20, 23, 39, 0.72, 0.72)    | 1.71e+01   | 4.19e-03   | nan        | nan        | nan      |
| (20, 23, 39, 0.7, 0.73)     | 5.54e+01   | 2.18e-02   | nan        | nan        | nan      |
| (20, 23, 39, 0.65, 0.78)    | 1.11e+00   | 2.18e-03   | nan        | nan        | nan      |
| (30, 11, 30, 0.6, 0.6)      | 3.79e-01   | 1.28e-04   | nan        | 2.70e+02   | 7.87e+01 |
| (30, 11, 30, 0.7, 0.7)      | 5.27e+00   | 6.66e-04   | nan        | nan        | nan      |
| (30, 11, 30, 0.8, 0.8)      | nan        | 5.78e-01   | nan        | nan        | nan      |
| (30, 11, 30, 0.81, 0.81)    | nan        | 9.63e-01   | nan        | nan        | nan      |
| (30, 11, 30, 0.82, 0.82)    | nan        | 3.55e-01   | nan        | nan        | nan      |
| (30, 11, 30, 0.84, 0.84)    | nan        | 7.91e-04   | nan        | nan        | nan      |
| (30, 11, 30, 0.88, 0.88)    | 2.14e-01   | 1.36e-05   | nan        | nan        | nan      |
| (100, 10, 10, 0.7, 0.7)     | 5.47e-02   | 5.20e-05   | nan        | nan        | nan      |
| (100, 10, 10, 0.8, 0.8)     | 4.22e+00   | 3.35e-04   | nan        | nan        | nan      |
| (100, 10, 10, 0.85, 0.85)   | 2.66e+02   | 2.57e-03   | nan        | nan        | nan      |
| (100, 10, 10, 0.9, 0.9)     | nan        | 1.66e-01   | nan        | nan        | nan      |
| (100, 10, 10, 0.92, 0.92)   | nan        | 6.62e+00   | nan        | nan        | nan      |
| (100, 10, 10, 0.94, 0.94)   | nan        | nan        | nan        | nan        | nan      |
| (100, 10, 10, 0.95, 0.95)   | nan        | nan        | nan        | nan        | nan      |
| (100, 10, 10, 0.97, 0.97)   | nan        | 9.51e-05   | nan        | nan        | nan      |
| (3, 100, 100, 0.1, 0.1)     | 1.07e-05   | 3.58e-06   | 1.04e-03   | 1.41e-03   | 1.33e-03 |
| (4, 100, 100, 0.15, 0.15)   | 2.79e-05   | 4.29e-06   | 2.41e-03   | 3.75e-03   | 3.75e-03 |
| (5, 100, 100, 0.2, 0.2)     | 3.53e-05   | 4.77e-06   | 5.17e-03   | 9.86e-03   | 9.49e-03 |
| (6, 100, 100, 0.25, 0.25)   | 9.51e-05   | 8.34e-06   | 1.00e-02   | 2.15e-02   | 2.42e-02 |
| (7, 50, 50, 0.35, 0.35)     | 8.58e-05   | 5.48e-06   | 6.16e-03   | 1.68e-02   | 1.30e-02 |
| (8, 50, 50, 0.4, 0.4)       | 1.92e-04   | 7.39e-06   | 9.49e-03   | 2.69e-02   | 3.52e-02 |
| (9, 50, 50, 0.45, 0.45)     | 5.81e-04   | 7.39e-06   | 8.32e-02   | 3.08e-01   | 1.42e-01 |
| (10, 50, 50, 0.5, 0.5)      | 7.66e-04   | 6.20e-06   | 3.08e-01   | 1.61e+00   | 7.55e-01 |
| (10, 10, 10, 0.74, 0.74)    | 2.55e-05   | 4.05e-06   | 1.13e-03   | 2.38e-03   | 3.81e-03 |
| (20, 12, 12, 0.86, 0.86)    | 1.56e-04   | 7.63e-06   | 6.78e-02   | nan        | 5.26e+02 |
| (30, 13, 13, 0.91, 0.91)    | 2.98e-02   | 1.10e-05   | 9.78e-01   | nan        | nan      |
| (40, 13, 13, 0.93, 0.93)    | 3.75e-01   | 1.62e-05   | nan        | nan        | nan      |
| (50, 14, 14, 0.94, 0.94)    | 1.91e+02   | 3.03e-05   | nan        | nan        | nan      |
| (60, 14, 14, 0.95, 0.95)    | 4.08e+02   | 4.67e-05   | nan        | nan        | nan      |
| (70, 14, 14, 0.96, 0.96)    | 2.58e+02   | 3.84e-05   | nan        | nan        | nan      |
| (10, 22, 22, 0.65, 0.65)    | 6.22e-05   | 4.77e-06   | 3.19e-03   | 3.93e-01   | 1.19e-01 |
| (20, 28, 28, 0.82, 0.82)    | 3.84e-03   | 8.34e-06   | 6.92e-02   | nan        | nan      |
| (30, 31, 31, 0.87, 0.87)    | 5.06e-01   | 1.45e-05   | 5.58e+01   | nan        | nan      |
| (10, 48, 48, 0.59, 0.59)    | 7.41e-05   | 5.25e-06   | 1.25e-02   | 1.16e+01   | 6.45e+00 |
| (20, 68, 68, 0.77, 0.77)    | 2.02e-02   | 1.05e-05   | 1.93e-01   | nan        | nan      |
| (5, 10, 0.1)                | 6.68e-06   | 3.58e-06   | 1.38e-04   | 8.73e-05   | 1.04e-04 |
| (5, 10, 0.2)                | 6.44e-06   | 3.34e-06   | 1.15e-04   | 8.70e-05   | 1.07e-04 |
| (5, 20, 0.05)               | 1.05e-05   | 3.58e-06   | 3.05e-04   | 2.80e-04   | 3.10e-04 |
| (5, 20, 0.1)                | 7.15e-06   | 3.10e-06   | 2.92e-04   | 2.17e-04   | 2.86e-04 |
| (5, 50, 0.01)               | 1.31e-05   | 3.81e-06   | 1.07e-03   | 1.13e-03   | 1.30e-03 |
| (5, 50, 0.02)               | 1.29e-05   | 3.58e-06   | 1.05e-03   | 1.12e-03   | 1.32e-03 |
| (10, 10, 0.4)               | 1.74e-05   | 4.77e-06   | 8.22e-04   | 2.25e-04   | 3.17e-04 |
| (10, 10, 0.6)               | 1.57e-05   | 3.81e-06   | 4.55e-04   | 2.30e-04   | 3.55e-04 |
| (10, 20, 0.3)               | 2.24e-05   | 4.53e-06   | 1.17e-03   | 9.31e-04   | 1.33e-03 |
| (10, 20, 0.5)               | 2.50e-05   | 4.29e-06   | 1.42e-03   | 1.20e-03   | 1.44e-03 |
| (10, 50, 0.05)              | 8.54e-05   | 5.25e-06   | 4.39e-03   | 4.63e-03   | 5.70e-03 |
| (10, 50, 0.1)               | 3.70e-05   | 5.96e-06   | 5.17e-03   | 4.74e-03   | 6.08e-03 |
| (10, 100, 0.01)             | 7.92e-05   | 5.96e-06   | 2.50e-02   | 2.38e-02   | 2.92e-02 |
| (10, 100, 0.02)             | 6.34e-05   | 8.82e-06   | 2.53e-02   | 2.22e-02   | 9.29e-02 |
| (20, 10, 0.6)               | 6.12e-04   | 2.34e-05   | 3.27e+00   | 1.26e-03   | 2.23e-03 |
| (20, 10, 0.7)               | 9.04e-05   | 1.74e-05   | 5.28e-01   | 1.29e-03   | 5.69e-03 |
| (20, 20, 0.5)               | 2.05e-03   | 3.39e-05   | 7.33e+00   | 7.28e-03   | 1.16e-01 |
| (20, 20, 0.6)               | 1.25e-04   | 9.78e-06   | 2.64e-02   | 1.03e-01   | 7.74e-01 |
| (20, 50, 0.3)               | 1.86e-01   | 4.15e-01   | nan        | 2.87e-02   | 4.18e+00 |
| (20, 50, 0.35)              | 3.27e-02   | 1.94e-03   | nan        | 2.60e-02   | 9.73e+00 |
| (20, 100, 0.2)              | 3.08e+00   | 5.33e+02   | nan        | 1.06e-01   | 9.11e+01 |
| (20, 100, 0.25)             | 6.99e-03   | 4.08e-01   | nan        | 1.04e-01   | 6.15e+02 |
| (50, 10, 0.83)              | 1.06e+00   | 3.44e-04   | nan        | nan        | 2.59e+02 |
| (50, 10, 0.85)              | 7.46e+00   | 8.02e-04   | nan        | nan        | nan      |
| (50, 20, 0.5)               | 2.38e-01   | 2.51e-02   | nan        | nan        | nan      |
| (50, 20, 0.6)               | 3.15e+00   | 2.37e-01   | nan        | nan        | nan      |
| (50, 20, 0.7)               | 2.01e+02   | 4.42e+01   | nan        | nan        | nan      |
| (50, 20, 0.71)              | 4.15e+02   | 2.23e+02   | nan        | nan        | nan      |
| (50, 20, 0.72)              | nan        | 3.48e+02   | nan        | nan        | nan      |
| (50, 20, 0.73)              | nan        | 2.93e+02   | nan        | nan        | nan      |
| (50, 20, 0.75)              | nan        | nan        | nan        | nan        | nan      |
| (50, 20, 0.76)              | nan        | 7.67e+01   | nan        | 3.11e+02   | nan      |
| (50, 20, 0.77)              | nan        | 1.02e+02   | nan        | nan        | nan      |
| (50, 20, 0.78)              | nan        | 1.54e+00   | nan        | nan        | nan      |
| (50, 20, 0.79)              | nan        | 6.06e-02   | nan        | 2.05e+02   | nan      |
| (50, 20, 0.8)               | nan        | 2.33e-03   | nan        | nan        | nan      |
| (50, 50, 0.1)               | 4.14e-02   | 5.16e+00   | nan        | nan        | nan      |
| (50, 50, 0.2)               | 1.41e-01   | 4.11e+01   | nan        | nan        | nan      |
| (50, 50, 0.3)               | 1.97e+00   | 2.31e+02   | nan        | nan        | nan      |
| (50, 50, 0.4)               | 2.80e+01   | nan        | nan        | nan        | nan      |
| (50, 50, 0.5)               | 7.69e+02   | nan        | nan        | nan        | nan      |
| (50, 50, 0.6)               | nan        | nan        | nan        | nan        | nan      |
| (50, 50, 0.71)              | nan        | nan        | nan        | nan        | nan      |
| (50, 50, 0.72)              | nan        | 1.45e+02   | nan        | nan        | nan      |
| (50, 50, 0.73)              | nan        | 2.16e-02   | nan        | nan        | nan      |
| (50, 50, 0.74)              | nan        | 1.04e-01   | nan        | 7.29e-01   | nan      |
| (50, 100, 0.1)              | 2.53e-01   | nan        | nan        | nan        | nan      |
| (50, 100, 0.2)              | 1.21e+01   | nan        | nan        | nan        | nan      |
| (50, 100, 0.3)              | 2.33e+02   | nan        | nan        | nan        | nan      |
| (50, 100, 0.4)              | nan        | nan        | nan        | nan        | nan      |
| (50, 100, 0.64)             | nan        | nan        | nan        | nan        | nan      |
| (50, 100, 0.65)             | nan        | nan        | nan        | nan        | nan      |
| (50, 100, 0.66)             | nan        | nan        | nan        | 5.80e+01   | nan      |
| (50, 100, 0.67)             | nan        | nan        | nan        | 2.12e+01   | nan      |
| (50, 100, 0.68)             | nan        | 2.10e+02   | nan        | nan        | nan      |
| (50, 100, 0.69)             | nan        | 9.81e+01   | nan        | 3.05e+00   | nan      |
| (50, 100, 0.7)              | nan        | 1.54e+01   | nan        | nan        | nan      |
| (100, 10, 0.6)              | 7.34e-03   | 1.17e-05   | nan        | nan        | nan      |
| (100, 10, 0.7)              | 2.55e-02   | 4.22e-05   | nan        | nan        | nan      |
| (100, 10, 0.8)              | 1.56e+00   | 1.07e-02   | nan        | nan        | nan      |
| (100, 20, 0.4)              | 5.21e-02   | 8.98e-04   | nan        | nan        | nan      |
| (100, 20, 0.5)              | 6.57e-01   | 8.69e-03   | nan        | nan        | nan      |
| (100, 20, 0.6)              | 4.66e+00   | 1.71e-02   | nan        | nan        | nan      |
| (100, 20, 0.7)              | 4.10e+02   | 6.54e+00   | nan        | nan        | nan      |
| (100, 20, 0.8)              | nan        | nan        | nan        | nan        | nan      |
| (100, 20, 0.89)             | nan        | nan        | nan        | nan        | nan      |
| (100, 20, 0.9)              | nan        | 2.77e+01   | nan        | nan        | nan      |
| (100, 50, 0.1)              | 1.79e-01   | 1.07e+01   | nan        | nan        | nan      |
| (100, 50, 0.2)              | 3.04e-01   | 5.61e+01   | nan        | nan        | nan      |
| (100, 50, 0.3)              | 8.21e+00   | 9.23e+02   | nan        | nan        | nan      |
| (100, 50, 0.4)              | 4.59e+01   | nan        | nan        | nan        | nan      |
| (100, 50, 0.5)              | nan        | nan        | nan        | nan        | nan      |
| (100, 50, 0.87)             | nan        | nan        | nan        | nan        | nan      |
| (100, 50, 0.88)             | nan        | 1.86e+00   | nan        | nan        | nan      |
| (100, 50, 0.89)             | nan        | 1.40e-02   | nan        | nan        | nan      |
| (100, 50, 0.9)              | nan        | 2.57e-04   | nan        | nan        | nan      |
| (100, 100, 0.1)             | 8.63e-01   | nan        | nan        | nan        | nan      |
| (100, 100, 0.2)             | 3.97e+01   | nan        | nan        | nan        | nan      |
| (100, 100, 0.3)             | 2.45e+02   | nan        | nan        | nan        | nan      |
| (100, 100, 0.4)             | nan        | nan        | nan        | nan        | nan      |
| (100, 100, 0.85)            | nan        | nan        | nan        | nan        | nan      |
| (100, 100, 0.86)            | nan        | 4.79e+01   | nan        | nan        | nan      |
| (100, 100, 0.87)            | nan        | 8.53e-03   | nan        | nan        | nan      |
| (100, 100, 0.88)            | nan        | 2.71e-04   | nan        | nan        | nan      |
| (100, 100, 0.89)            | nan        | 1.02e-04   | nan        | nan        | nan      |
| (100, 100, 0.9)             | nan        | 8.75e-05   | nan        | nan        | nan      |


## Finding all k-cliques

We time how long it takes to find all k-cliques.
We only record it, if it differs from the timing to check for k-cliques.

| Graph                       | kpkc       | FindClique | networkx |
  ---                         | ---        | ---        | ---
| (5, 50, 50, 0.15, 0.15)     | 6.54e-04   | 3.19e-05   | 1.23e-02 |
| (5, 50, 50, 0.2, 0.2)       | 8.53e-04   | 9.18e-05   | 2.34e-02 |
| (5, 50, 50, 0.25, 0.25)     | 2.46e-03   | 6.29e-04   | 4.48e-02 |
| (5, 50, 50, 0.0, 0.3)       | 7.22e-04   | 6.75e-05   | 1.50e-02 |
| (5, 50, 50, 0.0, 0.4)       | 1.93e-03   | 6.03e-04   | 3.23e-02 |
| (5, 50, 50, 0.0, 0.45)      | 2.44e-03   | 9.13e-04   | 3.68e-02 |
| (5, 50, 50, 0.0, 0.5)       | 6.94e-03   | 3.80e-03   | 5.69e-02 |
| (10, 26, 37, 0.49, 0.49)    | 2.64e-02   | 4.27e-04   | 5.79e+00 |
| (10, 26, 37, 0.5, 0.5)      | 5.42e-02   | 9.95e-04   | 1.25e+01 |
| (10, 26, 37, 0.51, 0.51)    | 5.73e-02   | 1.19e-03   | 1.19e+01 |
| (10, 26, 37, 0.4, 0.6)      | 3.95e-02   | 9.61e-04   | 8.72e+00 |
| (10, 26, 37, 0.3, 0.7)      | 6.50e-02   | 3.87e-03   | 1.31e+01 |
| (10, 50, 50, 0.42, 0.42)    | 9.74e-02   | 1.56e-03   | 2.07e+01 |
| (10, 50, 50, 0.43, 0.43)    | 1.20e-01   | 2.04e-03   | 2.71e+01 |
| (10, 50, 50, 0.44, 0.44)    | 1.64e-01   | 2.76e-03   | 3.47e+01 |
| (10, 50, 50, 0.46, 0.46)    | 3.31e-01   | 4.78e-03   | 5.39e+01 |
| (10, 50, 50, 0.48, 0.48)    | 5.91e-01   | 8.61e-03   | 8.35e+01 |
| (10, 50, 50, 0.5, 0.5)      | 9.65e-01   | 1.95e-02   | 1.35e+02 |
| (10, 50, 50, 0.4, 0.6)      | 1.18e+00   | 3.80e-02   | 1.57e+02 |
| (10, 50, 50, 0.0, 0.8)      | 1.69e+00   | 6.14e-01   | 9.99e+01 |
| (50, 5, 15, 0.918, 0.918)   | nan        | 3.51e+00   | nan      |
| (50, 5, 15, 0.92, 0.92)     | nan        | 3.08e+01   | nan      |
| (20, 23, 39, 0.71, 0.71)    | 8.63e+02   | 5.59e-01   | nan      |
| (20, 23, 39, 0.72, 0.72)    | nan        | 7.84e-01   | nan      |
| (20, 23, 39, 0.7, 0.73)     | 8.89e+02   | 5.07e-01   | nan      |
| (20, 23, 39, 0.65, 0.78)    | nan        | 1.23e+00   | nan      |
| (30, 11, 30, 0.84, 0.84)    | nan        | 7.25e+01   | nan      |
| (3, 100, 100, 0.1, 0.1)     | 3.13e-03   | 2.03e-03   | 7.52e-03 |
| (4, 100, 100, 0.15, 0.15)   | 5.55e-03   | 2.43e-03   | 4.37e-02 |
| (5, 100, 100, 0.2, 0.2)     | 1.36e-02   | 2.63e-03   | 2.06e-01 |
| (6, 100, 100, 0.25, 0.25)   | 4.18e-02   | 3.07e-03   | 1.06e+00 |
| (7, 50, 50, 0.35, 0.35)     | 1.91e-02   | 1.14e-03   | 8.59e-01 |
| (8, 50, 50, 0.4, 0.4)       | 4.67e-02   | 1.90e-03   | 3.96e+00 |
| (9, 50, 50, 0.45, 0.45)     | 2.07e-01   | 5.90e-03   | 2.27e+01 |
| (10, 50, 50, 0.5, 0.5)      | 1.13e+00   | 2.34e-02   | 1.52e+02 |
| (10, 10, 10, 0.74, 0.74)    | 3.44e-02   | 1.46e-02   | 1.05e+00 |
| (10, 22, 22, 0.65, 0.65)    | 4.42e-01   | 1.27e-01   | 2.57e+01 |
| (10, 48, 48, 0.59, 0.59)    | 2.44e+01   | 7.29e+00   | nan      |
| (5, 10, 0.1)                | 1.44e-04   | 9.92e-05   | 5.34e-04 |
| (5, 10, 0.2)                | 3.38e-04   | 2.48e-04   | 6.66e-04 |
| (5, 20, 0.05)               | 2.93e-03   | 2.34e-03   | 5.51e-03 |
| (5, 20, 0.1)                | 2.92e-03   | 2.32e-03   | 6.15e-03 |
| (5, 50, 0.01)               | 8.74e-02   | 7.38e-02   | 1.48e-01 |
| (5, 50, 0.02)               | 9.77e-02   | 8.26e-02   | 1.55e-01 |
| (10, 10, 0.4)               | 1.29e-03   | 5.85e-04   | 2.62e-02 |
| (10, 10, 0.6)               | 1.32e-02   | 7.08e-03   | 4.36e-02 |
| (10, 20, 0.3)               | 1.43e-02   | 7.44e-03   | 6.74e-01 |
| (10, 20, 0.5)               | 1.33e+00   | 9.36e-01   | 3.67e+00 |
| (10, 50, 0.05)              | 5.69e-02   | 6.87e-02   | 3.21e+01 |
| (10, 50, 0.1)               | 2.73e-01   | 2.34e-01   | 5.24e+01 |
| (10, 100, 0.01)             | 6.26e+00   | 8.61e+00   | nan      |
| (10, 100, 0.02)             | 9.31e+00   | 1.17e+01   | nan      |
| (20, 10, 0.6)               | 2.25e-03   | 8.82e-04   | 1.91e+01 |
| (20, 10, 0.7)               | 3.91e-01   | 1.54e-01   | 8.74e+01 |
| (20, 20, 0.5)               | 1.36e-01   | 1.44e-01   | nan      |
| (20, 20, 0.6)               | 1.58e+01   | 8.56e+00   | nan      |
| (20, 50, 0.3)               | 9.39e-01   | 2.84e+01   | nan      |
| (20, 50, 0.35)              | 4.19e+00   | 8.32e+01   | nan      |
| (20, 100, 0.2)              | 9.72e+00   | nan        | nan      |
| (20, 100, 0.25)             | 5.65e+01   | nan        | nan      |
| (50, 10, 0.83)              | 1.50e+01   | 5.76e+00   | nan      |
| (50, 10, 0.85)              | nan        | 1.22e+02   | nan      |

## Conclusions

`kpkc` and `FindClique` appear to be best choices for finding k-cliques in k-partite graphs.
- If all vertices are expected to have somewhat the same number of neighbors,
  then `FindClique` is the best choice.
- If there are many edges and the expected number of k-cliques is large,
  then `FindClique` is the best choice to obtain
  some k-cliques.
- If only few k-cliques (if any) are exepcted and
  vertices in larger parts have fewer neighbors
  then vertices in smaller parts, then `kpkc` is
  the best choice to obtain all k-cliques.
