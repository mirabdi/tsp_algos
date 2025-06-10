from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import time
import sys

class BaseTSPAlgorithm(ABC):
    """Base class for all TSP algorithms."""
    
    def __init__(self, max_dimension: Optional[int] = None):
        self._tour: Optional[List[int]] = None
        self._cost: Optional[float] = None
        self._runtime: Optional[float] = None
        self._memory_usage: Optional[int] = None
        self._max_dimension = max_dimension
    
    @property
    def name(self) -> str:
        """Return the name of the algorithm."""
        return self.__class__.__name__
    
    @property
    def complexity(self) -> str:
        """Return the time complexity of the algorithm."""
        raise NotImplementedError
    
    @property
    def max_dimension(self) -> Optional[int]:
        """Return the maximum dimension this algorithm can handle."""
        return self._max_dimension
    
    def check_dimension(self, dimension: int) -> None:
        """Check if the algorithm can handle the given dimension."""
        if self._max_dimension is not None and dimension > self._max_dimension:
            raise ValueError(
                f"{self.name} cannot handle datasets with dimension > {self._max_dimension}. "
                f"Current dimension: {dimension}"
            )
    
    @abstractmethod
    def solve(self, graph: List[List[float]]) -> None:
        """
        Solve the TSP problem for the given graph.
        
        Args:
            graph: Adjacency matrix representing the TSP graph
        """
        pass
    
    def get_tour(self) -> List[int]:
        """Return the computed tour."""
        if self._tour is None:
            raise RuntimeError("Algorithm has not been solved yet")
        return self._tour
    
    def get_cost(self) -> float:
        """Return the cost of the computed tour."""
        if self._cost is None:
            raise RuntimeError("Algorithm has not been solved yet")
        return self._cost
    
    def get_runtime(self) -> float:
        """Return the runtime of the algorithm in seconds."""
        if self._runtime is None:
            raise RuntimeError("Algorithm has not been solved yet")
        return self._runtime
    
    def get_memory_usage(self) -> int:
        """Return the memory usage of the algorithm in bytes."""
        if self._memory_usage is None:
            raise RuntimeError("Algorithm has not been solved yet")
        return self._memory_usage
    
    def _measure_performance(self, func):
        """Decorator to measure runtime and memory usage of the algorithm."""
        def wrapper(*args, **kwargs):
            # Measure initial memory usage
            initial_memory = sys.getsizeof(self)
            
            # Measure runtime
            start_time = time.process_time()  # CPU time instead of wall-clock time
            result = func(*args, **kwargs)
            self._runtime = time.process_time() - start_time
            
            # Measure final memory usage
            final_memory = sys.getsizeof(self)
            self._memory_usage = final_memory - initial_memory
            
            return result
        return wrapper 