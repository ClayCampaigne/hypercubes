"""
Visualization components for hypercubes
"""

import numpy as np
from copy import copy
from typing import List, Optional
import ipywidgets as widgets
from ipywidgets import FloatSlider, IntSlider, VBox, HBox
from bqplot import LinearScale, Axis, Lines, Figure

from .core import NDCube
from .utils import rotmat


class HypercubeWidget:
    """
    Interactive widget for visualizing and manipulating n-dimensional hypercubes.
    """
    
    def __init__(self, ndims: int = 4, figsize: tuple = (6, 6), 
                 axis_range: tuple = (-2.0, 2.0)):
        """
        Initialize the hypercube visualization widget.
        
        Args:
            ndims: Number of dimensions for the hypercube
            figsize: Figure size as (width, height)
            axis_range: Axis range as (min, max) for both x and y axes
        """
        self.ndims = ndims
        self.figsize = figsize
        self.axis_range = axis_range
        
        # Initialize the hypercube
        self.cube = NDCube(ndims=self.ndims)
        
        # Set up the plot
        self._setup_plot()
        
        # Set up controls
        self._setup_controls()
        
        # Apply initial rotations for better default view
        self._apply_initial_rotations()
        
        # Create the complete widget
        self._create_widget()
        
    def _setup_plot(self):
        """Set up the bqplot figure and scales."""
        # Create scales
        self.x_sc = LinearScale(min=self.axis_range[0], max=self.axis_range[1])
        self.y_sc = LinearScale(min=self.axis_range[0], max=self.axis_range[1])
        
        # Create axes
        self.ax_x = Axis(scale=self.x_sc)
        self.ax_y = Axis(scale=self.y_sc, orientation='vertical')
        
        # Create lines for each edge
        proj = self.cube.parproject()
        self.lines = []
        for ed in proj:
            line = Lines(
                x=[point[0] for point in ed], 
                y=[point[1] for point in ed], 
                scales={'x': self.x_sc, 'y': self.y_sc}
            )
            self.lines.append(line)
        
        # Create the figure
        self.figure = Figure(
            marks=self.lines, 
            axes=[self.ax_x, self.ax_y],
            title=f'{self.ndims}D Hypercube Manipulator',
            animation_duration=100,
            figsize=self.figsize,
            min_aspect_ratio=1.0,
            max_aspect_ratio=1.0
        )
    
    def _setup_controls(self):
        """Set up the control sliders."""
        # Dimension selector
        self.ndims_slider = IntSlider(
            min=2, max=8, step=1, value=self.ndims,
            description='Dimensions:',
            style={'description_width': 'initial'}
        )
        self.ndims_slider.observe(self._on_ndims_change, 'value')
        
        # Rotation sliders (one for each pair of dimensions)
        self._create_rotation_sliders()
        
    def _create_rotation_sliders(self):
        """Create rotation sliders for the current number of dimensions."""
        self.rotation_sliders = []
        self.slider_values = []
        
        # Default rotation values for 4D cube to look more interesting
        default_rotations = [1.4, 3.7, 4.6] if self.ndims == 4 else [0.0] * (self.ndims - 1)
        
        for i in range(self.ndims - 1):
            initial_value = default_rotations[i] if i < len(default_rotations) else 0.0
            slider = FloatSlider(
                min=0, max=2*np.pi, step=0.1, value=initial_value,
                description=f'Rotate 0→{i+1}:',
                style={'description_width': 'initial'},
                readout_format='.2f'
            )
            slider.observe(self._update_plot, 'value')
            self.rotation_sliders.append(slider)
            self.slider_values.append(initial_value)
    
    def _create_widget(self):
        """Create the complete widget layout."""
        controls = [self.ndims_slider] + self.rotation_sliders
        self.controls_box = VBox(controls)
        self.widget = VBox([self.figure, self.controls_box])
    
    def _apply_initial_rotations(self):
        """Apply initial rotations to make the default view more interesting."""
        for i, slider in enumerate(self.rotation_sliders):
            if slider.value != 0.0:
                rotation_matrix = rotmat(0, i+1, slider.value, self.ndims)
                self.cube.lintransform(rotation_matrix)
        
        # Update the visualization with rotated cube
        newproj = self.cube.parproject()
        for i in range(len(self.lines)):
            if i < len(newproj):
                self.lines[i].x = [elem[0] for elem in newproj[i]]
                self.lines[i].y = [elem[1] for elem in newproj[i]]
    
    def _on_ndims_change(self, change):
        """Handle dimension change."""
        new_ndims = change['new']
        if new_ndims != self.ndims:
            self.ndims = new_ndims
            self._rebuild_visualization()
    
    def _rebuild_visualization(self):
        """Rebuild the entire visualization for new dimensions."""
        # Create new cube
        self.cube = NDCube(ndims=self.ndims)
        
        # Update figure title
        self.figure.title = f'{self.ndims}D Hypercube Manipulator'
        
        # Create new lines
        proj = self.cube.parproject()
        new_lines = []
        for ed in proj:
            line = Lines(
                x=[point[0] for point in ed], 
                y=[point[1] for point in ed], 
                scales={'x': self.x_sc, 'y': self.y_sc}
            )
            new_lines.append(line)
        
        # Update figure marks
        self.lines = new_lines
        self.figure.marks = self.lines
        
        # Recreate rotation sliders
        self._create_rotation_sliders()
        
        # Update controls layout
        controls = [self.ndims_slider] + self.rotation_sliders
        self.controls_box.children = controls
    
    def _update_plot(self, change):
        """Update the plot when sliders change."""
        # Apply rotations based on slider changes
        for i in range(len(self.rotation_sliders)):
            rotation_delta = self.rotation_sliders[i].value - self.slider_values[i]
            if abs(rotation_delta) > 1e-10:  # Only rotate if there's a meaningful change
                rotation_matrix = rotmat(0, i+1, rotation_delta, self.ndims)
                self.cube.lintransform(rotation_matrix)
                self.slider_values[i] = copy(self.rotation_sliders[i].value)
        
        # Update the visualization
        newproj = self.cube.parproject()
        for i in range(len(self.lines)):
            if i < len(newproj):  # Safety check
                self.lines[i].x = [elem[0] for elem in newproj[i]]
                self.lines[i].y = [elem[1] for elem in newproj[i]]
    
    def display(self):
        """Display the widget."""
        return self.widget
    
    def reset_rotations(self):
        """Reset all rotations to zero."""
        for slider in self.rotation_sliders:
            slider.value = 0.0


def create_hypercube_widget(ndims: int = 4, **kwargs) -> HypercubeWidget:
    """
    Convenience function to create a hypercube widget.
    
    Args:
        ndims: Number of dimensions
        **kwargs: Additional arguments passed to HypercubeWidget
        
    Returns:
        HypercubeWidget instance
    """
    return HypercubeWidget(ndims=ndims, **kwargs)