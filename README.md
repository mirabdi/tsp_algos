# TSP Algorithms Implementation

This project implements various algorithms for solving the Traveling Salesman Problem (TSP) using both Python and C++ (via pybind11). The implementations include both exact and approximation algorithms.

## Project Structure

```
tsp_algos/
├── algorithms/
│   ├── cpp/                    # C++ implementations
├── data/
│   └── dataset.py            # Dataset loading and processing
├── analysis/
│   └── performance.py        # Performance analysis tools
├── datasets/                 # TSP dataset files
├── results/                  # Output directory for results
├── main.py                  # Main script to run algorithms
├── setup.py                 # Build configuration
└── requirements.txt         # Python dependencies
```

## Implemented Algorithms

1. **Brute Force** (max dimension: 12)
   - Time complexity: O(n!)
   - Finds the optimal solution by trying all possible permutations

2. **Held-Karp** (max dimension: 20)
   - Time complexity: O(n²2ⁿ)
   - Dynamic programming approach for optimal solution

3. **Greedy** (max dimension: 100,000)
   - Time complexity: O(n²)
   - Always chooses the nearest unvisited city

4. **MST Approximation** (max dimension: 100,000)
   - Time complexity: O(E log V)
   - 2-approximation algorithm using minimum spanning tree


6. **Convex Hull** (max dimension: 100,000)
   - Time complexity: O(n²)
   - Uses convex hull and MST for interior points

## Available Datasets

The project includes a range of test datasets:
- Small datasets (5-100 cities): sample_5 through sample_100
- Medium datasets: a280 (280 cities), xql662 (662 cities)
- Large datasets: kz9976 (9976 cities), mona-lisa100K (100,000 cities)

## Setup and Installation

### Prerequisites

- Python, C++, Cmake

### Installation Steps

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Build the C++ extensions:
```bash
python setup.py build_ext --inplace
```

## Usage

The main script `main.py` can be used to run and compare different algorithms on various datasets:

```bash
python main.py
```

This will:
1. Process each dataset in the `datasets/` directory
2. Run applicable algorithms on each dataset based on their maximum supported dimensions
3. Measure performance metrics (runtime, memory usage, tour cost)
4. Save results to the `results/` directory

### Adding New Datasets

Place TSP dataset files in the `datasets/` directory. The files should be in TSPLIB format with a `.tsp` extension.

### Adding New Algorithms

1. Create C++ implementation in `algorithms/cpp/`
2. Add the algorithm to `setup.py` in the `ext_modules` list
3. Rebuild the extensions

## Performance Analysis

The `analysis/performance.py` module provides tools for:
- Measuring algorithm runtime
- Tracking memory usage
- Comparing tour costs
- Generating performance reports

Results are saved in JSON format in the `results/` directory.
