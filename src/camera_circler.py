"""Turn a camera around a point.

Classes:
    CameraCircler
"""

import math

from pygame import Vector3

from camera import Camera
from camera_controller import CameraController
from config import CAMERA_SPEED

__author__ = "Jye-Ming Serres"


class CameraCircler(CameraController):
    """Points a camera towards a point a turns around it.

    Attributes:
        camera (:obj:`Camera`): The camera to control.

    Methods:
        update()
    """

    def __init__(
            self,
            camera: Camera,
            center: Vector3,
            angular_reference: Vector3,
            inverted: bool = False) -> None:
        """Creates an instance with the camera to control.

        Args:
            camera: The camera to control.
            center: xxx
            angular_reference: xxx
        """
        super().__init__(camera)
        self._center = center
        self._angular_reference = angular_reference
        self._inverted = inverted

        self._cycle_origin = Vector3(camera.aperture - self._center)
        self._cycle_arm = Vector3(camera.aperture - self._center)
        self._radius = self._cycle_origin.length()
        if self._radius == 0:
            raise ValueError("circle radius is zero")

        self._angle = 0
        self._speed = CAMERA_SPEED
        self._direction = -1 if inverted else 1

        self._point_center()

    def update(self, dt: float) -> None:
        dist_travelled = dt * self._speed * self._direction
        rad_travelled = dist_travelled / (2 * math.pi * self._radius)

        self._cycle_arm.rotate_rad_ip(rad_travelled ,self._angular_reference)

        self.camera.aperture = self._center + self._cycle_arm
        self._point_center()

    def _point_center(self) -> None:
        new_image_x = self._angular_reference.cross(self._cycle_arm).normalize()
        new_image_y = self._angular_reference.normalize()
        self.camera.set_orientation(new_image_x, new_image_y)
