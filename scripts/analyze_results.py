import json
import os
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_results_table():
    # Get all JSON files from results directory
    results_dir = Path("results")
    json_files = list(results_dir.glob("*.json"))
    
    # Initialize lists to store data
    data = []
    
    # Read each JSON file
    for json_file in json_files:
        with open(json_file, 'r') as f:
            result = json.load(f)
            
            # Extract relevant information
            row = {
                'Algorithm': result['algorithm'],
                'Dataset': result['dataset'],
                'Time (s)': f"{result['runtime']:.6f}",
                'Memory (KB)': f"{result['memory_usage'] / 1024:.2f}",
                'Tour Cost': f"{result['tour_cost']:.2f}"
            }
            data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by Algorithm and Dataset
    df = df.sort_values(['Algorithm', 'Dataset'])
    
    # Create pivot tables
    pivot_time = df.pivot(index='Algorithm', columns='Dataset', values='Time (s)')
    pivot_memory = df.pivot(index='Algorithm', columns='Dataset', values='Memory (KB)')
    pivot_cost = df.pivot(index='Algorithm', columns='Dataset', values='Tour Cost')
    
    # Create Excel writer
    output_file = Path("results") / "analysis_results.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write raw data
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        # Write pivot tables
        pivot_time.to_excel(writer, sheet_name='Runtime')
        pivot_memory.to_excel(writer, sheet_name='Memory Usage')
        pivot_cost.to_excel(writer, sheet_name='Tour Cost')
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
    
    print(f"Results have been written to {output_file}")
    return df

if __name__ == "__main__":
    generate_results_table() 