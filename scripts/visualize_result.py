import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def read_tsp_file(tsp_file):
    """Read coordinates from TSP file."""
    coordinates = {}
    reading_coords = False
    
    with open(tsp_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                reading_coords = True
                continue
            elif line == "EOF":
                break
                
            if reading_coords:
                parts = line.split()
                if len(parts) == 3:
                    city_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    coordinates[city_id] = (x, y)
    
    return coordinates

def visualize_tour(result_name):
    """Visualize TSP tour from result file."""
    # Read the result file
    result_file = Path("results") / f"{result_name}.json"
    with open(result_file, 'r') as f:
        result = json.load(f)
    
    # Get dataset name and read coordinates
    dataset = result['dataset']
    tsp_file = Path("datasets") / f"{dataset}.tsp"
    coordinates = read_tsp_file(tsp_file)
    
    # Extract tour and adjust indices (add 1 to match TSP file indexing)
    tour = [city + 1 for city in result['tour']]
    
    # Create plot
    plt.figure(figsize=(10, 8))
    
    # Plot cities
    x_coords = [coordinates[city][0] for city in coordinates]
    y_coords = [coordinates[city][1] for city in coordinates]
    plt.scatter(x_coords, y_coords, c='blue', s=100, label='Cities')
    
    # Plot tour path
    tour_x = [coordinates[city][0] for city in tour]
    tour_y = [coordinates[city][1] for city in tour]
    plt.plot(tour_x, tour_y, 'r-', linewidth=2, label='Tour Path')
    
    # Add city labels
    for city, (x, y) in coordinates.items():
        plt.annotate(str(city), (x, y), xytext=(5, 5), textcoords='offset points')
    
    # Customize plot
    plt.title(f'TSP Tour - {result["algorithm"]} on {dataset}\nTour Cost: {result["tour_cost"]:.2f}')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    output_file = Path("visualizations") / f"{result_name}_tour.png"
    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file)
    plt.close()
    
    print(f"Visualization saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize_result.py <result_name>")
        print("Example: python visualize_result.py ConvexHull_sample_15")
        sys.exit(1)
    
    result_name = sys.argv[1]
    visualize_tour(result_name) 