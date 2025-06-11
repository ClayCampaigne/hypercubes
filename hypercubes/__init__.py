"""
Hypercubes: Interactive n-dimensional hypercube visualization
"""

from .core import NDCube, OccludingCube
from .visualization import HypercubeWidget, create_hypercube_widget
from .utils import rotmat

__version__ = "0.1.0"
__all__ = ["NDCube", "OccludingCube", "HypercubeWidget", "create_hypercube_widget", "rotmat"]