import json
import os
from tabulate import tabulate
from collections import defaultdict

def analyze_results():
    # Get all JSON files from results directory
    results_dir = "results"
    json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    
    # Group files by dataset
    datasets = set()
    algorithms = set()
    for file in json_files:
        # Extract dataset name (e.g., 'a280' from 'ConvexHull_a280.json')
        dataset = file.split('_')[1].split('.')[0]
        algorithm = file.split('_')[0]
        datasets.add(dataset)
        algorithms.add(algorithm)
    
    # Sort for consistent output
    datasets = sorted(list(datasets))
    algorithms = sorted(list(algorithms))
    
    # Create tables for each metric
    metrics = {
        'runtime': 'Runtime (seconds)',
        'dimension': 'Dimension',
        'tour_cost': 'Tour Cost',
        'ground_truth': 'Ground Truth',
        'approximation_ratio': 'Approximation Ratio'
    }
    
    # Process each metric
    for metric, header in metrics.items():
        print(f"\n{header} Comparison:")
        print("-" * 80)
        
        # Prepare data for table
        table_data = []
        headers = ['Dataset'] + list(algorithms)
        
        for dataset in datasets:
            row = [dataset]
            for algorithm in algorithms:
                filename = f"{algorithm}_{dataset}.json"
                filepath = os.path.join(results_dir, filename)
                
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        value = data.get(metric, 'N/A')
                        # Format runtime to 6 decimal places
                        if metric == 'runtime':
                            value = f"{value:.6f}"
                        # Format approximation ratio to 4 decimal places
                        elif metric == 'approximation_ratio':
                            value = f"{value:.4f}"
                        row.append(value)
                except (FileNotFoundError, json.JSONDecodeError):
                    row.append('N/A')
            
            table_data.append(row)
        
        # Print table
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

if __name__ == "__main__":
    analyze_results() 