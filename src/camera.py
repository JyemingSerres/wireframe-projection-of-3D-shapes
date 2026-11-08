"""Use a virtual camera to control the position and movement of the view.

Classes:
    Camera
"""

from pygame import Vector3

__author__ = "Jye-Ming Serres"


class Camera:
    """Embodies a set of states, parameters and necessary data for viewing shapes.

    Attributes:
        rectilinear_velocity (:obj:`pygame.Vector3`): The camera's current velocity in 
            pixels/seconds.
        angular_velocity (:obj:`pygame.Vector3`): The camera's current counterclockwise angular 
            velocity in degrees/second around `image_y` (yaw), `image_x` (pitch) then 
            `orientation` (roll), in that order.

    Methods:
        update()
        move()
        rotate()
    """

    def __init__(self, aperture: Vector3, focal_length: float) -> None:
        """Creates an instance with a fixed focal length at the specified position.

        Args:
            aperture: Position of the aperture/position of the camera.
            focal_length: Distance between the aperture and the image plane. Influences FOV.
        """
        self.aperture = aperture
        self._image_x = Vector3(0, -1, 0)
        self._image_y = Vector3(0, 0, 1)
        self._orientation = self._calculate_orientation()
        self._focal_length = focal_length

        self.rectilinear_velocity = Vector3(0, 0, 0)
        self.angular_velocity = Vector3(0, 0, 0)

    @property
    def image_x(self) -> Vector3:
        """Direction of the x coordinate of the image. (normalized)"""
        return self._image_x

    @property
    def image_y(self) -> Vector3:
        """Direction of the y coordinate of the image. (normalized)"""
        return self._image_y

    @property
    def orientation(self) -> Vector3:
        """The camera's direction. (normalized)"""
        return self._orientation

    @property
    def focal_length(self) -> float:
        """Distance between the aperture and the image plane. Influences FOV."""
        return self._focal_length

    def set_orientation(self, image_x: Vector3, image_y: Vector3) -> None:
        """Sets the orientation.

        Args:
            image_x: The new image_x.
            image_y: The new image_y.

        Raises:
            ValueError: The passed vectors are not perpendicular.
        """
        if image_x.dot(image_y) != 0:
            raise ValueError("New camera orientation vectors should be perpendicular")
        self._image_x = image_x.normalize()
        self._image_y = image_y.normalize()
        self._orientation = self._calculate_orientation()

    def update(self, dt: float) -> None:
        """Applies the camera's rectilinear and angular velocity accross a time interval.

        Args:
            dt: Delta time (seconds).   
        """
        self.move(self.rectilinear_velocity * dt)
        self.rotate(self.angular_velocity * dt)

    def move(self, displacement: Vector3) -> None:
        self.aperture += displacement

    def rotate(self, angular_displacement: Vector3) -> None:
        """Rotates the camera around its aperture.

        Args:
            angular_displacement: Counterclockwise rotation in degrees around `image_y` (yaw), 
                `image_x` (pitch) then `orientation` (roll), in that order.
        """
        self._image_x.rotate_ip(angular_displacement[0], self._image_y) # yaw
        self._image_y.rotate_ip(angular_displacement[1], self._image_x) # pitch
        self._orientation = self._calculate_orientation()
        self._image_x.rotate_ip(angular_displacement[2], self._orientation) # roll
        self._image_y.rotate_ip(angular_displacement[2], self._orientation) # roll

    def _calculate_orientation(self) -> Vector3:
        """Calculates the orientation of the camera.

        The orientation is a vector normal to the image plane.

        Returns:
            Orientation vector. (normalized)
        """
        return self._image_y.cross(self._image_x).normalize()
