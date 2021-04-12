from time import time
from kpkc.test import get_random_k_partite_graph, get_random_k_partite_graph_2, load_tester
from cysignals.alarm import *
from sage.all import *
import multiprocessing as mp

timeout = 1000

def obtain_tester(*args):
    if len(args) == 1:
        return load_tester("sample_graphs/{}.gz".format(args[0]))
    elif len(args) == 5:
        return get_random_k_partite_graph(*args)
    else:
        return get_random_k_partite_graph_2(*args)

def format_number(f):
    return "{0:4.2e}".format(f)

def benchmark_instance_with_alg(G, G1, alg):
    output = {}
    if alg in ['kpkc', 'bitCLQ', 'networkx']:
        try:
            alarm(timeout)
            out = G.benchmark(alg)
            output['first'] = format_number(next(out))
            output['all'] = format_number(next(out))
        except (KeyboardInterrupt, RuntimeError):
            if not 'first' in output:
                output['first'] = "----    "
            if not 'all' in output:
                output['all'] = "----    "
        finally:
            cancel_alarm()

    else:
        assert G1
        try:
            alarm(timeout)
            a = time()
            G1.clique_number(algorithm=alg)
            b = time()
            output['first'] = format_number(b-a)
        except (KeyboardInterrupt, RuntimeError):
            output['first'] = "----    "
        finally:
            cancel_alarm()


    return output

def benchmark_instance(args, verbose=True):
    output = {}
    G = obtain_tester(*args)

    algorithms = ['kpkc', 'bitCLQ', 'networkx', 'Cliquer', 'mcqd']
    G1 = Graph(G.edges)

    for alg in algorithms:
        output[alg] = benchmark_instance_with_alg(G, G1, alg)

    # Remove 'all' if it is the same as 'first'.

    if all(output[alg]['all'] == output[alg]['first'] for alg in algorithms if 'all' in output[alg]):
        for alg in algorithms:
            if 'all' in output[alg]:
                del output[alg]['all']

    if all(output[alg]['all'] == "----    " for alg in algorithms if 'all' in output[alg]):
        for alg in algorithms:
            if 'all' in output[alg]:
                del output[alg]['all']

    if verbose:
        print(args, output)

    return output

instances = [
        [0],
        [1],
        [2],
        [20],
        [100],
        [1000],
        [10000],
        [1000000],
        [2000000],
        [5000000],
        [10000000],
        [5, 50, 50, 0.14, 0.14],
        [5, 50, 50, 0.15, 0.15],
        [5, 50, 50, 0.20, 0.20],
        [5, 50, 50, 0.25, 0.25],
        [5, 50, 50, 0.0, 0.3],
        [5, 50, 50, 0.0, 0.4],
        [5, 50, 50, 0.0, 0.45],
        [5, 50, 50, 0.0, 0.5],
        [10, 26, 37, 0.49, 0.49],
        [10, 26, 37, 0.50, 0.50],
        [10, 26, 37, 0.51, 0.51],
        [10, 26, 37, 0.40, 0.60],
        [10, 26, 37, 0.30, 0.70],
        [10, 50, 50, 0.42, 0.42],
        [10, 50, 50, 0.43, 0.43],
        [10, 50, 50, 0.44, 0.44],
        [10, 50, 50, 0.46, 0.46],
        [10, 50, 50, 0.48, 0.48],
        [10, 50, 50, 0.5, 0.5],
        [10, 50, 50, 0.4, 0.6],
        [10, 50, 50, 0.0, 0.8],
        [50, 5, 15, 0.91, 0.91],
        [50, 5, 15, 0.918, 0.918],
        [50, 5, 15, 0.92, 0.92],
        [20, 23, 39, 0.70, 0.70],
        [20, 23, 39, 0.71, 0.71],
        [20, 23, 39, 0.72, 0.72],
        [20, 23, 39, 0.70, 0.73],
        [20, 23, 39, 0.65, 0.78],
        [30, 11, 30, 0.60, 0.60],
        [30, 11, 30, 0.70, 0.70],
        [30, 11, 30, 0.80, 0.80],
        [30, 11, 30, 0.81, 0.81],
        [30, 11, 30, 0.82, 0.82],
        [30, 11, 30, 0.84, 0.84],
        [30, 11, 30, 0.88, 0.88],
        [100, 10, 10, 0.70, 0.70],
        [100, 10, 10, 0.80, 0.80],
        [100, 10, 10, 0.85, 0.85],
        [100, 10, 10, 0.90, 0.90],
        [100, 10, 10, 0.92, 0.92],
        [100, 10, 10, 0.94, 0.94],
        [100, 10, 10, 0.95, 0.95],
        [100, 10, 10, 0.97, 0.97],
        [3, 100, 100, 0.1, 0.1],
        [4, 100, 100, 0.15, 0.15],
        [5, 100, 100, 0.2, 0.2],
        [6, 100, 100, 0.25, 0.25],
        [7, 50, 50, 0.35, 0.35],
        [8, 50, 50, 0.4, 0.4],
        [9, 50, 50, 0.45, 0.45],
        [10, 50, 50, 0.5, 0.5],
        [10, 10, 10, 0.74, 0.74],
        [20, 12, 12, 0.86, 0.86],
        [30, 13, 13, 0.91, 0.91],
        [40, 13, 13, 0.93, 0.93],
        [50, 14, 14, 0.94, 0.94],
        [60, 14, 14, 0.95, 0.95],
        [70, 14, 14, 0.96, 0.96],
        [10, 22, 22, 0.65, 0.65],
        [20, 28, 28, 0.82, 0.82],
        [30, 31, 31, 0.87, 0.87],
        [10, 48, 48, 0.59, 0.59],
        [20, 68, 68, 0.77, 0.77],
        [5, 10, 0.1],
        [5, 10, 0.2],
        [5, 20, 0.05],
        [5, 20, 0.1],
        [5, 50, 0.01],
        [5, 50, 0.02],
        [10, 10, 0.4],
        [10, 10, 0.6],
        [10, 20, 0.3],
        [10, 20, 0.5],
        [10, 50, 0.05],
        [10, 50, 0.1],
        [10, 100, 0.01],
        [10, 100, 0.02],
        [20, 10, 0.6],
        [20, 10, 0.7],
        [20, 20, 0.5],
        [20, 20, 0.6],
        [20, 50, 0.3],
        [20, 50, 0.35],
        [20, 100, 0.2],
        [20, 100, 0.25],
        [50, 10, 0.83],
        [50, 10, 0.85],
        [50, 20, 0.5],
        [50, 20, 0.6],
        [50, 20, 0.7],
        [50, 20, 0.71],
        [50, 20, 0.72],
        [50, 20, 0.73],
        [50, 20, 0.75],
        [50, 20, 0.76],
        [50, 20, 0.77],
        [50, 20, 0.78],
        [50, 20, 0.79],
        [50, 20, 0.8],
        [50, 50, 0.1],
        [50, 50, 0.2],
        [50, 50, 0.3],
        [50, 50, 0.4],
        [50, 50, 0.5],
        [50, 50, 0.6],
        [50, 50, 0.71],
        [50, 50, 0.72],
        [50, 50, 0.73],
        [50, 50, 0.74],
        [50, 100, 0.1],
        [50, 100, 0.2],
        [50, 100, 0.3],
        [50, 100, 0.4],
        [50, 100, 0.64],
        [50, 100, 0.65],
        [50, 100, 0.66],
        [50, 100, 0.67],
        [50, 100, 0.68],
        [50, 100, 0.69],
        [50, 100, 0.7],
        [100, 10, 0.6],
        [100, 10, 0.7],
        [100, 10, 0.8],
        [100, 20, 0.4],
        [100, 20, 0.5],
        [100, 20, 0.6],
        [100, 20, 0.7],
        [100, 20, 0.8],
        [100, 20, 0.89],
        [100, 20, 0.9],
        [100, 50, 0.1],
        [100, 50, 0.2],
        [100, 50, 0.3],
        [100, 50, 0.4],
        [100, 50, 0.5],
        [100, 50, 0.87],
        [100, 50, 0.88],
        [100, 50, 0.89],
        [100, 50, 0.9],
        [100, 100, 0.1],
        [100, 100, 0.2],
        [100, 100, 0.3],
        [100, 100, 0.4],
        [100, 100, 0.85],
        [100, 100, 0.86],
        [100, 100, 0.87],
        [100, 100, 0.88],
        [100, 100, 0.89],
        [100, 100, 0.9],
        ]

all_algs = ('kpkc', 'bitCLQ', 'networkx')
first_algs = all_algs + ('Cliquer', 'mcqd')

def print_instance(instance):
    if len(instance) == 1:
        return "{}".format(instance[0])
    else:
        return "{}".format(tuple(instance))

def run_benchmarks(n_threads=1):
    pool = mp.Pool(n_threads)
    results = pool.map(benchmark_instance, instances)
    print('done')
    with open('all.md', 'w') as a:
        with open('first.md', 'w') as f:
            a.write('{:28}| {:10} | {:10} | {}\n'.format('graph', *all_algs))
            f.write('{:28}| {:10} | {:10} | {:10} | {:10} | {}\n'.format('graph', *first_algs))

            for i,instance in enumerate(instances):
                print(instance)
                out = results[i]
                print(out)
                f.write('{:28}| {:10} | {:10} | {:10} | {:10} | {}\n'.format(
                    print_instance(instance), *[out[alg]['first'] for alg in first_algs]))
                if 'all' in out['kpkc']:
                    a.write('{:28}| {:10} | {:10} | {}\n'.format(
                        print_instance(instance), *[out[alg]['all'] for alg in all_algs]))
