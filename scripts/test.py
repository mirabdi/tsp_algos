from ..algorithms.cpp.mst_approximation import MSTApproximation
from ..algorithms.cpp.greedy import GreedyTSP
from ..algorithms.cpp.brute_force import BruteForceTSP
from ..algorithms.cpp.held_karp import HeldKarpTSP

# Create a simple test graph
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# Test MST Approximation
mst = MSTApproximation()
mst.solve(graph)
print("MST Tour:", mst._tour)
print("MST Cost:", mst._cost)

# Test Greedy
greedy = GreedyTSP()
greedy.solve(graph)
print("\nGreedy Tour:", greedy._tour)
print("Greedy Cost:", greedy._cost)

# Test Brute Force (for small graphs)
bf = BruteForceTSP()
bf.solve(graph)
print("\nBrute Force Tour:", bf._tour)
print("Brute Force Cost:", bf._cost)

# Test Held-Karp (for small graphs)
hk = HeldKarpTSP()
hk.solve(graph)
print("\nHeld-Karp Tour:", hk._tour)
print("Held-Karp Cost:", hk._cost)