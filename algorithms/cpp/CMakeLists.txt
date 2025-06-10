cmake_minimum_required(VERSION 3.4)
project(tsp_algorithms)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Add all extensions
pybind11_add_module(mst_approximation mst_approximation.cpp)
pybind11_add_module(greedy greedy.cpp)
pybind11_add_module(brute_force brute_force.cpp)
pybind11_add_module(held_karp held_karp.cpp)
pybind11_add_module(own_convex_hull own_convex_hull.cpp)

# Set C++ standard for all targets
set_target_properties(mst_approximation greedy brute_force held_karp own_convex_hull PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
) 