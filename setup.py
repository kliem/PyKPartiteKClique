from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize
import sys

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name='kpkc',
    version='0.1.0',
    description='A python interface to the KPartiteKClique',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kliem/PyKPartiteKClique',
    author='Jonathan Kliem',
    author_email='jonathan.kliem@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    ext_modules=cythonize([
        Extension(
            "kpkc",
            sources=["pykpkc/kpkc.pyx", "KPartiteKClique/kpkc.cpp"],
            language="c++",
            include_dirs=["KPartiteKClique", "pykpkc"],
            depends=["KPartiteKClique/kpkc.h", "pykpkc/kpkc.pxd"]),
        Extension(
            "_kpkc_memory_allocator",
            sources=["pykpkc/_kpkc_memory_allocator.pyx"],
            language="c++",
            include_dirs=["pykpkc"],
            depends=["pykpkc/_kpkc_memory_allocator.pxd"])],
        language_level=3),
    zip_safe=False,
    python_requires='>=3.6',
    package_dir = {'kpkc': 'pykpkc'},
    install_requires=["cysignals", "Cython"],
    include_dirs=["KPartiteKClique", "pykpkc"] + sys.path,
    package_dirs=["KPartiteKClique", "pykpkc"],
    package_data={"kpkc": ["*.pxd", "*.h"]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics']
    )
