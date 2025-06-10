import random
import math
from pathlib import Path
import numpy as np

def generate_tsp_file(n: int, output_file: Path) -> None:
    """
    Generate a TSP file with n random cities.
    
    Args:
        n: Number of cities
        output_file: Path to output file
    """
    # Generate random coordinates in a 1000x1000 grid
    coordinates = np.random.randint(0, 1000, size=(n, 2))
    
    # Write TSP file
    with open(output_file, 'w') as f:
        # Write header
        f.write(f"NAME : sample_{n}\n")
        f.write(f"COMMENT : Sample TSP instance with {n} cities\n")
        f.write("TYPE : TSP\n")
        f.write(f"DIMENSION : {n}\n")
        f.write("EDGE_WEIGHT_TYPE : EUC_2D\n")
        f.write("NODE_COORD_SECTION\n")
        
        # Write coordinates
        for i, (x, y) in enumerate(coordinates, 1):
            f.write(f"{i} {x} {y}\n")
        
        # Write footer
        f.write("EOF\n")

def main():
    # Create datasets directory if it doesn't exist
    dataset_dir = Path('datasets')
    dataset_dir.mkdir(exist_ok=True)
    
    # Generate sample datasets
    dimensions = [5*i for i in range(1, 21)]
    for n in dimensions:
        output_file = dataset_dir / f"sample_{n}.tsp"
        print(f"Generating sample_{n}.tsp...")
        generate_tsp_file(n, output_file)
        print(f"Generated {output_file}")

if __name__ == "__main__":
    main() 