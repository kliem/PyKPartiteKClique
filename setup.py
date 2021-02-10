from setuptools import setup
from Cython.Build import cythonize

setup(
        name='kpkc',
        ext_modules=cythonize("kpkc.pyx"),
        zip_safe=False,
        )
