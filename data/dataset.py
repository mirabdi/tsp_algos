from typing import List, Dict, Optional
from .tsp_parser import TSPParser
import json
from pathlib import Path

class TSPDataset:
    """Class for handling TSP datasets."""
    
    def __init__(self, file_path: str):
        """
        Initialize a TSP dataset from a file.
        
        Args:
            file_path: Path to the TSP file
        """
        self._file_path = file_path
        self._parser = TSPParser()
        self._data: Optional[Dict] = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Load and parse the TSP file."""
        # Load and parse the TSP file
        self._data = self._parser.parse_file(self._file_path)
    
    @property
    def dimension(self) -> int:
        """Return the dimension of the TSP instance."""
        if not self._data:
            raise RuntimeError("Dataset not loaded")
        return self._data['dimension']
    
    @property
    def coordinates(self) -> List[tuple]:
        """Return the coordinates of the cities."""
        if not self._data:
            raise RuntimeError("Dataset not loaded")
        return self._data['coordinates']
    
    @property
    def distance_matrix(self) -> List[List[float]]:
        """Return the distance matrix, calculating distances on demand."""
        if not self._data:
            raise RuntimeError("Dataset not loaded")
        
        n = self.dimension
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Calculate distances on demand
        for i in range(n):
            for j in range(i + 1, n):
                dist = self.get_distance(i, j)
                matrix[i][j] = dist
                matrix[j][i] = dist
                
        return matrix
    
    def get_distance(self, i: int, j: int) -> float:
        """
        Get the distance between two cities.
        
        Args:
            i: Index of first city
            j: Index of second city
            
        Returns:
            Distance between cities i and j
        """
        if not self._data:
            raise RuntimeError("Dataset not loaded")
        
        if i == j:
            return 0.0
            
        # Calculate distance on demand
        p1 = self.coordinates[i]
        p2 = self.coordinates[j]
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    
    def calculate_tour_cost(self, tour: List[int]) -> float:
        """
        Calculate the total cost of a tour.
        
        Args:
            tour: List of city indices representing the tour
            
        Returns:
            Total cost of the tour
        """
        if not self._data:
            raise RuntimeError("Dataset not loaded")
        
        cost = 0.0
        for i in range(len(tour)):
            j = (i + 1) % len(tour)
            cost += self.get_distance(tour[i], tour[j])
        return cost 