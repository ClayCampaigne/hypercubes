"""
Utility functions for hypercube operations
"""

import numpy as np


def rotmat(dim1: int, dim2: int, theta: float, ndims: int) -> np.ndarray:
    """
    Matrix for rotating dim1 into dim2 by theta radians, 
    for a ndims-dimensional set of points
    
    Args:
        dim1: First dimension index
        dim2: Second dimension index  
        theta: Rotation angle in radians
        ndims: Total number of dimensions
        
    Returns:
        Rotation matrix as numpy array
    """
    mat = np.zeros((ndims, ndims), float)
    mat[dim1, dim1] = np.cos(theta)
    mat[dim2, dim2] = np.cos(theta)
    mat[dim1, dim2] = np.sin(theta)
    mat[dim2, dim1] = -np.sin(theta)
    for dim in range(ndims):
        if dim not in (dim1, dim2):
            mat[dim, dim] = 1.0
    return mat