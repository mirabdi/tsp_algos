from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import setuptools

__version__ = '0.0.1'

class get_pybind_include(object):
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

ext_modules = [
    Extension(
        'algorithms.cpp.mst_approximation',
        ['algorithms/cpp/mst_approximation.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
    Extension(
        'algorithms.cpp.greedy',
        ['algorithms/cpp/greedy.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
    Extension(
        'algorithms.cpp.brute_force',
        ['algorithms/cpp/brute_force.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
    Extension(
        'algorithms.cpp.held_karp',
        ['algorithms/cpp/held_karp.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
    Extension(
        'algorithms.cpp.own_convex_hull',
        ['algorithms/cpp/own_convex_hull.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
]

setup(
    name='tsp_algorithms',
    version=__version__,
    author='Your Name',
    author_email='your.email@example.com',
    description='TSP algorithms with C++ implementations',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0'],
    setup_requires=['pybind11>=2.6.0'],
    zip_safe=False,
) 