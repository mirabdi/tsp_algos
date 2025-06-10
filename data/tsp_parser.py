from typing import List, Tuple, Dict, Optional
import re

class TSPParser:
    """Parser for TSP file format."""
    
    def __init__(self):
        self._dimension: Optional[int] = None
        self._coordinates: List[Tuple[float, float]] = []
    
    def parse_file(self, file_path: str) -> Dict:
        """
        Parse a TSP file and return the graph data.
        
        Args:
            file_path: Path to the TSP file
            
        Returns:
            Dictionary containing the parsed data
        """
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse header
        self._parse_header(content)
        
        # Parse coordinates
        self._parse_coordinates(content)
        
        return {
            'dimension': self._dimension,
            'coordinates': self._coordinates
        }
    
    def _parse_header(self, content: str) -> None:
        """Parse the header section of the TSP file."""
        # Extract dimension
        dimension_match = re.search(r'DIMENSION\s*:\s*(\d+)', content)
        if dimension_match:
            self._dimension = int(dimension_match.group(1))
        else:
            raise ValueError("Dimension not found in TSP file")
    
    def _parse_coordinates(self, content: str) -> None:
        """Parse the coordinates section of the TSP file."""
        # Find the start of coordinates section
        coord_section = re.search(r'NODE_COORD_SECTION\s*(.*?)(?=EOF|\Z)', 
                                content, re.DOTALL)
        if not coord_section:
            raise ValueError("Coordinates section not found in TSP file")
        
        # Parse coordinates
        coord_pattern = r'(\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)'
        matches = re.finditer(coord_pattern, coord_section.group(1))
        
        self._coordinates = []
        for match in matches:
            node_id = int(match.group(1))
            x = float(match.group(2))
            y = float(match.group(3))
            self._coordinates.append((x, y))
        
        if len(self._coordinates) != self._dimension:
            raise ValueError(f"Expected {self._dimension} coordinates, "
                           f"but found {len(self._coordinates)}") 