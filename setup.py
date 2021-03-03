from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_py import build_py as setuptools_build_py
from distutils.command.build_ext import build_ext as du_build_ext
import os
import sys

class build_py(setuptools_build_py):
    def run(self):
        self.distribution.package_data['pykpkc'] += ['memory_allocator.pxd', 'pykpkc.pxd']
        setuptools_build_py.run(self)

class build_ext(du_build_ext):
    def run(self):
        from Cython.Build.Dependencies import cythonize
        self.distribution.ext_modules[:] = cythonize(
        self.distribution.ext_modules,
        language_level=3)
        du_build_ext.run(self)

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

extensions = [
#    Extension(
#        "kpkc.kpkc",
#        sources=["kpkc/kpkc.pyx", "KPartiteKClique/kpkc.cpp"],
#        language="c++",
#        include_dirs=["KPartiteKClique"],
#        extra_compile_args=["-std=c++11"],
#        depends=["KPartiteKClique/kpkc.h", "kpkc/kpkc.pxd"]),
    Extension(
        "pykpkc.memory_allocator",
        sources=["pykpkc/memory_allocator.pyx"],
        language="c++",
        extra_compile_args=["-std=c++11"],
        include_dirs=[os.path.dirname(__file__) or "."],
#        depends=["memory_allocator.pxd"]
        )
]

setup(
    name='pykpkc',
    version='0.1.0',
    description='A python interface to the KPartiteKClique',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kliem/PyKPartiteKClique',
    author='Jonathan Kliem',
    author_email='jonathan.kliem@gmail.com',
    license='GPLv3',
    packages=['pykpkc'],
    #packages=find_packages(),
    ext_modules=extensions,
#    zip_safe=False,
    python_requires='>=3.6',
    package_dir = {'pykpkc': 'pykpkc'},
    install_requires=["cysignals", "Cython"],
    include_dirs=[os.path.dirname(__file__) or "." ,"KPartiteKClique"] + sys.path,
    package_data={"pykpkc": ["*.pxd", "*.h"]},
    cmdclass = {'build_py': build_py,
                'build_ext': build_ext},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics']
    )
