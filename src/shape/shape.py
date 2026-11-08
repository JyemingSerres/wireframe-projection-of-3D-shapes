"""Provides the base class for shapes.

Classes:
    Shape
"""

from pygame import Vector3

from config import Color

__author__ = "Jye-Ming Serres"


class Shape:
    """Parent class for shapes within the simulation.

    Generic manipulations of shapes should be based on this definition.

    Attributes:
        rectilinear_velocity (:obj:`pygame.Vector3`): The shape's current velocity in 
            pixels/seconds.
        angular_velocity (:obj:`pygame.Vector3`): The shape's current counterclockwise angular 
            velocity in degrees/seconds around the x, y, z axis.

    Methods:
        update()
        move()
        rotate()
    """

    def __init__(self, center: Vector3,
                 vertices: list[Vector3],
                 edges: list[tuple[int, int]],
                 color: Color) -> None:
        """Creates an instance from specified vertices, edges and shape color.

        args:
            center: Used as a basis for some manipulations like rotation.
            vertices: List of 3D vectors representing each the coordinates of a vertex.
            edges: Association table between vertices. Each tuple (an edge) contains the index of 
                both connecting vertices within the list of 3D vectors.
            color: Color used to draw the shape.
        """
        self._center = center
        self._vertices = vertices
        self._edges = edges
        self._color = color

        self.rectilinear_velocity = Vector3(0, 0, 0)
        self.angular_velocity = Vector3(0, 0, 0)

    @property
    def center(self) -> Vector3:
        """Used as a basis for some manipulations like rotation."""
        return self._center

    @property
    def vertices(self) -> list[Vector3]:
        """List of 3D vectors representing each the coordinates of a vertex."""
        return self._vertices

    @property
    def edges(self) -> list[tuple[int, int]]:
        """Association table between vertices. 
        
        Each tuple (an edge) contains the index of the connecting vertices within the shape's list 
        of vertices.
        """
        return self._edges

    @property
    def color(self) -> Color:
        """Color used to draw the shape."""
        return self._color

    def update(self, dt: float) -> None:
        """Applies the shape's rectilinear and angular velocity accross a time interval.

        Args:
            dt: Delta time (seconds).   
        """
        self.move(self.rectilinear_velocity * dt)
        self.rotate(self.angular_velocity * dt)

    def move(self, displacement: Vector3) -> None:
        displacement = displacement.copy() # Shallow copy
        for vertex in self._vertices:
            vertex += displacement
        self._center += displacement

    def rotate(self, angular_displacement: Vector3) -> None:
        """Rotates the shape around its center.

        Args:
            angular_displacement: Counterclockwise rotation in degrees around the x, y, z axis.
        """
        center_pos = self._center.copy() # Shallow copy for the second move() call.
        self.move(-center_pos)
        for vertex in self._vertices:
            vertex.rotate_x_ip(angular_displacement.x)
            vertex.rotate_y_ip(angular_displacement.y)
            vertex.rotate_z_ip(angular_displacement.z)
        self.move(center_pos)
