"""Provides the model of the program.

Classes:
    World
"""

from camera.camera import Camera
from shape.shape import Shape


class World:
    """Contains the shapes and the camera. Acts as the model of the program.

    Methods:
        update()
    """

    def __init__(self, camera: Camera, shapes: list[Shape]) -> None:
        """Creates an instance containing the camera and shapes.

        Args:
            camera: A virtual camera controlled by the end user.
            shapes: The shapes that make up the world.
        """
        self._shapes = shapes
        self._camera = camera

    @property
    def shapes(self) -> list[Shape]:
        return self._shapes

    @property
    def camera(self) -> Camera:
        return self._camera

    def update(self, dt: float) -> None:
        """Steps the camera and every shape across a time interval.

        Args:
            dt: Delta time (seconds).
        """
        for shape in self._shapes:
            shape.update(dt)
        self._camera.update(dt)
