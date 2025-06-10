from typing import List, Dict, Any, Tuple, Callable
from data.dataset import TSPDataset
import time
import sys
import json
from pathlib import Path
import psutil
import os
import pandas as pd

# Ground truth values for known optimal tour lengths
GROUND_TRUTH = {
    'a280': 2579,    # Known optimal tour length for a280
    'xql662': 2513,  # Known optimal tour length for xql662
    'kz9976': 106188 # Known optimal tour length for kz9976
}

class PerformanceAnalyzer:
    """Class for analyzing algorithm performance."""
    
    def __init__(self):
        self._results: Dict[str, Dict[str, Any]] = {}
        self._process = psutil.Process(os.getpid())
    
    def _load_existing_result(self, algorithm_name: str, dataset_name: str, output_dir: str = 'results') -> Dict[str, Any]:
        """
        Load an existing result from a JSON file.
        
        Args:
            algorithm_name: Name of the algorithm
            dataset_name: Name of the dataset
            output_dir: Directory containing the results
            
        Returns:
            Dictionary containing the result, or None if not found
        """
        result_file = Path(output_dir) / f"{algorithm_name}_{dataset_name}.json"
        if result_file.exists():
            with open(result_file, 'r') as f:
                return json.load(f)
        return None
    
    def _save_individual_result(self, result: Dict[str, Any], output_dir: str = 'results') -> None:
        """
        Save an individual algorithm result to a JSON file.
        
        Args:
            result: Dictionary containing the algorithm result
            output_dir: Directory to save the result
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate filename from algorithm and dataset names
        key = f"{result['algorithm']}_{result['dataset']}"
        output_file = Path(output_dir) / f"{key}.json"
        
        # Add ground truth comparison if available
        if result['dataset'] in GROUND_TRUTH:
            ground_truth = GROUND_TRUTH[result['dataset']]
            result['ground_truth'] = ground_truth
            result['approximation_ratio'] = result['tour_cost'] / ground_truth if result['tour_cost'] is not None else None
        
        # Save to JSON file
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
    
    def analyze_algorithm(self, 
                         algorithm: Tuple[str, Callable],
                         dataset: TSPDataset,
                         dataset_name: str) -> Dict[str, Any]:
        """
        Analyze the performance of an algorithm on a dataset.
        
        Args:
            algorithm: Tuple of (algorithm_name, algorithm_function)
            dataset: TSP dataset to use
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary containing performance metrics
        """
        algorithm_name, algorithm_func = algorithm
        
        # Check for existing result first
        existing_result = self._load_existing_result(algorithm_name, dataset_name)
        if existing_result:
            print(f"Using existing result for {algorithm_name} on {dataset_name}")
            return existing_result
            
        # Measure initial memory
        initial_memory = self._process.memory_info().rss
        
        # Measure runtime
        start_time = time.time()
        
        # Solve the TSP problem
        tour, cost = algorithm_func(dataset.distance_matrix)
        
        # Calculate metrics
        runtime = time.time() - start_time
        final_memory = self._process.memory_info().rss
        memory_usage = final_memory - initial_memory
        
        # Store results
        result = {
            'algorithm': algorithm_name,
            'dataset': dataset_name,
            'dimension': dataset.dimension,
            'runtime': runtime,
            'memory_usage': memory_usage,
            'tour_cost': cost,
            'tour': tour
        }
        
        # Store in results dictionary
        key = f"{algorithm_name}_{dataset_name}"
        self._results[key] = result
        
        # Save result immediately
        self._save_individual_result(result)
        
        return result
    
    def compare_algorithms(self,
                          algorithms: List[Tuple[str, Callable]],
                          dataset: TSPDataset,
                          dataset_name: str) -> Dict[str, Any]:
        """
        Compare multiple algorithms on the same dataset.
        
        Args:
            algorithms: List of (algorithm_name, algorithm_function) tuples
            dataset: TSP dataset to use
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary containing comparison results
        """
        comparison = {
            'dataset': dataset_name,
            'dimension': dataset.dimension,
            'algorithms': {}
        }
        
        total_algorithms = len(algorithms)
        for i, algorithm in enumerate(algorithms, 1):
            algorithm_name = algorithm[0]
            print(f"\nProcessing algorithm {i}/{total_algorithms}: {algorithm_name}")
            try:
                result = self.analyze_algorithm(algorithm, dataset, dataset_name)
                comparison['algorithms'][algorithm_name] = {
                    'runtime': result['runtime'],
                    'memory_usage': result['memory_usage'],
                    'tour_cost': result['tour_cost']
                }
                print(f"Completed {algorithm_name} in {result['runtime']:.2f} seconds")
            except Exception as e:
                print(f"Error running {algorithm_name}: {str(e)}")
                comparison['algorithms'][algorithm_name] = {
                    'error': str(e),
                    'runtime': None,
                    'memory_usage': None,
                    'tour_cost': None
                }
        
        return comparison
    
    def save_results(self, output_dir: str = 'results') -> None:
        """
        Save analysis results to JSON files and Excel.
        
        Args:
            output_dir: Directory to save results
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save individual results as JSON
        for key, result in self._results.items():
            output_file = Path(output_dir) / f"{key}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
        
        # Prepare data for Excel
        excel_data = []
        for key, result in self._results.items():
            algo_name, dataset_name = key.split('_', 1)
            row = {
                'Dataset': dataset_name,
                'Algorithm': algo_name,
                'Dimension': result['dimension'],
                'Runtime (s)': result['runtime'] if result['runtime'] is not None else 'Error',
                'Memory Usage (KB)': result['memory_usage'] / 1024 if result['memory_usage'] is not None else 'Error',
                'Tour Cost': result['tour_cost'] if result['tour_cost'] is not None else 'Error'
            }
            excel_data.append(row)
        
        # Create DataFrame and save to Excel
        df = pd.DataFrame(excel_data)
        
        # Sort by dataset name and algorithm name
        df = df.sort_values(['Dataset', 'Algorithm'])
        
        # Save to Excel with formatting
        excel_file = Path(output_dir) / 'results.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')
            
            # Get the worksheet
            worksheet = writer.sheets['Results']
            
            # Adjust column widths
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
    
    def get_results(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all results.
        
        Returns:
            Dictionary containing all results
        """
        return self._results 