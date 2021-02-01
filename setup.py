from setuptools import setup
from Cython.Build import cythonize

setup(
        name='k_partite_k_clique',
        ext_modules=cythonize("k_partite_k_clique.pyx"),
        zip_safe=False,
        )
