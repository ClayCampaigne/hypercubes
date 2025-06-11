"""
Core hypercube classes
"""

import numpy as np
from itertools import product
from typing import List, Tuple, Optional


class NDCube:
    """
    N-dimensional hypercube class.
    Only the init method is specific to cubes.
    """
    
    def __init__(self, ndims: int = 4, center: bool = True, verbose: bool = False):
        """
        Initialize an n-dimensional hypercube.
        
        Args:
            ndims: Number of dimensions
            center: Whether to center the cube at origin
            verbose: Whether to print debug information
        """
        self.ndims = ndims
        self.v = [np.array(xyz) for xyz in product(*[[0., 1.],] * ndims)]
        self.e = []  # the edges are the *indexes* of the vertices in the vertex list

        # build list of edges quadratically by checking adjacency
        for i in range(len(self.v)):
            for j in range(i + 1, len(self.v)):
                if verbose:
                    print(f"comparing {self.v[i]} and {self.v[j]}")
                    print(f"diff is {np.sum(np.abs(self.v[i] - self.v[j]))}")
                if np.sum(np.abs(self.v[i] - self.v[j])) == 1:
                    self.e += [(i, j)]
                    if verbose:
                        print(f"we added {self.v[i]} - {self.v[j]}")
        
        if center:
            self.translate(np.array([-0.5] * self.ndims))
            
    def lintransform(self, matrix: np.ndarray) -> None:
        """
        Linearly transform the shape by multiplying all vertices by matrix.
        
        Args:
            matrix: Transformation matrix
        """
        for i in range(len(self.v)):
            self.v[i] = matrix @ self.v[i]
            
    def translate(self, vector: np.ndarray) -> None:
        """
        Translate all vertices by the given vector.
        
        Args:
            vector: Translation vector
        """
        for i in range(len(self.v)):
            self.v[i] += vector
        
    def get_edges(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Get all edges as pairs of vertex coordinates.
        
        Returns:
            List of edge tuples (start_vertex, end_vertex)
        """
        return [(self.v[e[0]], self.v[e[1]]) for e in self.e]
    
    def parproject(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Parallel projection onto 2D: return the first two coordinates of each point.
        
        Returns:
            List of projected edge tuples in 2D
        """
        return [(self.v[e[0]][:2], self.v[e[1]][:2]) for e in self.e]


class OccludingCube:
    """
    Attempt to implement 'Back Face Culling'
    https://www.gabrielgambetta.com/computer-graphics-from-scratch/hidden-surface-removal.html
    
    Note: This is incomplete implementation attempting back-face culling for hidden surface removal.
    """
    
    def __init__(self, ndims: int = 4, center: bool = True, verbose: bool = False):
        """
        Initialize an n-dimensional hypercube with occlusion support.
        
        Args:
            ndims: Number of dimensions
            center: Whether to center the cube at origin
            verbose: Whether to print debug information
        """
        self.ndims = ndims
        self.v = [np.array(xyz) for xyz in product(*[[0., 1.],] * ndims)]
        self.e = []  # the edges are the *indexes* of the vertices in the vertex list
        self.f = []  # the faces - indexes of edges belonging to front faces vs not

        # build list of edges quadratically by checking adjacency
        for i in range(len(self.v)):
            for j in range(i + 1, len(self.v)):
                if verbose:
                    print(f"comparing {self.v[i]} and {self.v[j]}")
                    print(f"diff is {np.sum(np.abs(self.v[i] - self.v[j]))}")
                if np.sum(np.abs(self.v[i] - self.v[j])) == 1:
                    self.e += [(i, j)]
                    if verbose:
                        print(f"we added {self.v[i]} - {self.v[j]}")
                        
        # TODO: construct list of faces with normal vectors
        # Face construction is incomplete - would need to:
        # 1. Find all points that share the same value in one dimension
        # 2. Calculate normal vectors for each face
        # 3. Determine front-facing vs back-facing based on viewer position
        
        for d in range(self.ndims):
            for b in (0., 1.):
                pass  # Face construction placeholder
        
        if center:
            self.translate(np.array([-0.5] * self.ndims))
            
    def lintransform(self, matrix: np.ndarray) -> None:
        """
        Linearly transform the shape by multiplying all vertices by matrix.
        
        Args:
            matrix: Transformation matrix
        """
        for i in range(len(self.v)):
            self.v[i] = matrix @ self.v[i]
            
    def translate(self, vector: np.ndarray) -> None:
        """
        Translate all vertices by the given vector.
        
        Args:
            vector: Translation vector
        """
        for i in range(len(self.v)):
            self.v[i] += vector
        
    def get_edges(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Get all edges as pairs of vertex coordinates.
        
        Returns:
            List of edge tuples (start_vertex, end_vertex)
        """
        return [(self.v[e[0]], self.v[e[1]]) for e in self.e]
    
    def parproject(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Parallel projection onto 2D: return the first two coordinates of each point.
        
        Returns:
            List of projected edge tuples in 2D
        """
        return [(self.v[e[0]][:2], self.v[e[1]][:2]) for e in self.e]