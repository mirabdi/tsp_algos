from algorithms.cpp.mst_approximation import MSTApproximation as CppMSTApproximation
from algorithms.cpp.held_karp import HeldKarpTSP as CppHeldKarpTSP
from algorithms.cpp.brute_force import BruteForceTSP as CppBruteForceTSP
from algorithms.cpp.greedy import GreedyTSP as CppGreedyTSP
from algorithms.cpp.own_convex_hull import OwnConvexHullTSP as CppOwnConvexHullTSP
from data.dataset import TSPDataset
from analysis.performance import PerformanceAnalyzer
import os
from pathlib import Path
import time
import psutil
import gc
import json

def get_dataset_dimension(tsp_file: Path) -> int:
    """Get the dimension of a TSP dataset without loading the entire file."""
    with open(tsp_file, 'r') as f:
        for line in f:
            if line.startswith('DIMENSION'):
                return int(line.split(':')[1].strip())
    raise ValueError(f"Dimension not found in {tsp_file}")

def check_existing_results(dataset_name: str, algorithm_name: str) -> bool:
    """Check if results already exist for a dataset and algorithm combination."""
    results_dir = Path('results')
    result_file = results_dir / f"{dataset_name}_{algorithm_name}.json"
    return result_file.exists()

def create_algorithm_wrapper(algorithm_class, name):
    """Create a wrapper function that returns tour and cost."""
    def wrapper(distance_matrix):
        algo = algorithm_class()
        algo.solve(distance_matrix)
        return algo.get_tour(), algo.get_cost()
    return name, wrapper

def main():
    # Initialize analyzer
    analyzer = PerformanceAnalyzer()
    
    # List of available datasets
    datasets = [
        'a280',          
        'xql662',        
        'kz9976',        
        'mona-lisa100K', 
    ]
    
    # Initialize all algorithms with their max dimensions
    algorithms = [
        (CppBruteForceTSP, "BruteForce", 12),      
        (CppHeldKarpTSP, "HeldKarp", 20),         
        (CppGreedyTSP, "Greedy", 90000),         
        (CppMSTApproximation, "MSTApproximation", 90000), 
        (CppOwnConvexHullTSP, "ConvexHull", 90000), 
    ]
    
    # Process each dataset
    dataset_dir = Path('datasets')
    for dataset_name in datasets:
        tsp_file = dataset_dir / f"{dataset_name}.tsp"
        if not tsp_file.exists():
            print(f"\nSkipping {dataset_name} - file not found")
            continue
            
        print(f"\nProcessing dataset: {dataset_name}")
        
        try:
            # Get dimension first
            dimension = get_dataset_dimension(tsp_file)
            print(f"Dataset dimension: {dimension}")
            
            # Filter algorithms that can handle this dimension
            applicable_algorithms = [
                create_algorithm_wrapper(algo_class, name)
                for algo_class, name, max_dim in algorithms 
                if max_dim is None or dimension <= max_dim
            ]
            
            if not applicable_algorithms:
                print(f"No algorithms can handle dimension {dimension}")
                continue
                
            # Load dataset only for applicable algorithms
            dataset = TSPDataset(str(tsp_file))
            
            # Compare algorithms
            comparison = analyzer.compare_algorithms(
                applicable_algorithms,
                dataset,
                dataset_name
            )
            
            # Print results
            print("\nResults:")
            for algo_name, metrics in comparison['algorithms'].items():
                print(f"\n{algo_name}:")
                if 'error' in metrics:
                    print(f"  Error: {metrics['error']}")
                else:
                    print(f"  Runtime: {metrics['runtime']:.2f} seconds")
                    print(f"  Memory Usage: {metrics['memory_usage'] / 1024:.2f} KB")
                    print(f"  Tour Cost: {metrics['tour_cost']:.2f}")
            
        except Exception as e:
            print(f"Error processing {dataset_name}: {str(e)}")
        finally:
            # Force garbage collection after each dataset
            gc.collect()
    
    print("\nAll results have been saved to the 'results' directory")

if __name__ == "__main__":
    main() 