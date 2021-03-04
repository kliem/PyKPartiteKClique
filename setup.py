from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_py import build_py as setuptools_build_py
from distutils.command.build_ext import build_ext as du_build_ext
from distutils.command.build import build as _build
from Cython.Build.Dependencies import cythonize
import os
import sys

class build_py(setuptools_build_py):
    def run(self):
#        self.distribution.package_data['kpkc'] += ['memory_allocator.pxd', 'kpkc.pxd']
        setuptools_build_py.run(self)

class build_ext(du_build_ext):
    def run(self):
        from Cython.Build.Dependencies import cythonize
        self.distribution.ext_modules[:] = cythonize(
        self.distribution.ext_modules,
#        include_path=['kpkc'] + sys.path,
        build_dir="build",
        include_path=['build', ''] + sys.path,
        compiler_directives={'embedsignature': True},
        language_level=3)
        du_build_ext.run(self)

from glob import glob

opj = os.path.join


cythonize_dir = "build"

# Run Distutils
class build(_build):
    def run(self):
        """
        Run Cython first.
        """
        dist = self.distribution
        ext_modules = dist.ext_modules
        if ext_modules:
            dist.ext_modules[:] = self.cythonize(ext_modules)

        _build.run(self)

    def cythonize(self, extensions):
        # Run Cython with -Werror on continuous integration services
        # with Python 3.6 or later
        if "CI" in os.environ and sys.version_info >= (3, 6):
            from Cython.Compiler import Options
            Options.warning_errors = True

        from Cython.Build.Dependencies import cythonize
        return cythonize(extensions,
                build_dir=cythonize_dir,
                include_path=["", cythonize_dir],
                compiler_directives=dict(binding=True, language_level=2))


with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

extensions = [
    Extension(
        "kpkc.kpkc",
        sources=["kpkc/kpkc.pyx", "kpkc/KPartiteKClique/kpkc.cpp"],
        language="c++"),
    Extension(
        "kpkc.memory_allocator",
        sources=["kpkc/memory_allocator.pyx"],
        language="c++",
        extra_compile_args=["-std=c++11"],
#        include_dirs=[os.path.dirname(__file__) or "."],
#        depends=["memory_allocator.pxd"]
        )
]

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
    ext_modules=cythonize(extensions, language_level=3),
    zip_safe=False,
    python_requires='>=3.6',
    package_dir = {'kpkc': 'kpkc'},
    install_requires=["cysignals", "Cython"],
#    include_dirs=["kpkc" ,"KPartiteKClique"] + sys.path,
    package_data={"kpkc": ["*.pxd", "*.h", "KPartiteKClique/*.h", "KPartiteKClique/*.cpp"]},
    #cmdclass = {'build': build},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics']
    )
