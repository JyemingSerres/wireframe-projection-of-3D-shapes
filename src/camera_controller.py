"""Manage controls over a camera.

Classes:
    CameraController
"""

from abc import ABC, abstractmethod

from camera import Camera

__author__ = "Jye-Ming Serres"


class CameraController(ABC):
    """Base class to control a camera.

    Attributes:
        camera (:obj:`Camera`): The camera to control.

    Methods:
        update()
    """

    def __init__(self, camera: Camera) -> None:
        """Creates an instance with the camera to control.

        Args:
            camera: The camera to control.
        """
        self.camera = camera

    @abstractmethod
    def update(self, dt: float) -> None:
        """Reevaluates the camera's state."""
