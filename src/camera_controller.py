"""Manage controls over a camera.

Classes:
    CameraController
    SCam
    SCamLateralLeft
    SCamLateralRight
    SCamLateralNeutral
    SCamMedialFront
    SCamMedialBack
    SCamMedialNeutral
    SCamVerticalUp
    SCamVerticalDown
    SCamVerticalNeutral
"""

from enum import Enum, unique

from pygame import Vector3

from config import CAMERA_LOOK_SENS, CAMERA_SPEED
from state_machine import State, StateMachine
from camera import Camera

__author__ = "Jye-Ming Serres"


@unique
class CamEvent(Enum):
    LEFT_SHIFT = 1,
    RIGHT_SHIFT = 2,
    FORWARD_SHIFT = 3,
    BACKWARD_SHIFT = 4,
    UP_SHIFT = 5,
    DOWN_SHIFT = 6


class CameraController:
    """Connects pygame events and inputs to the camera. 

    Attributes:
        camera (:obj:`Camera`): The camera to control.
        look_sens (`float`): A coefficient dictating how much the mouse influences camera rotation.
        speed (`int`): The speed at which the camera travels in pixels/second.
        sm_medial (:obj:`StateMachine`): State machine governing the camera's medial movements.
        sm_lateral (:obj:`StateMachine`): State machine governing the camera's lateral movements.
        sm_vertical (:obj:`StateMachine`): State machine governing the camera's vertical movements.

    Methods:
        translate_event()
        rotate_event()
        update()
    """

    def __init__(self, camera: Camera) -> None:
        """Creates an instance with the camera to control.

        Args:
            camera: The camera to control.
        """
        self.camera = camera
        self.look_sens = CAMERA_LOOK_SENS
        self.speed = CAMERA_SPEED
        self._rel_direction = Vector3(0, 0, 0)

        # medial translation state machine
        medial_neutral = SCamMedialNeutral(self._rel_direction)
        medial_front = SCamMedialFront(self._rel_direction)
        medial_back = SCamMedialBack(self._rel_direction)
        self.sm_medial = StateMachine([medial_neutral, medial_front, medial_back])
        self.sm_medial.add_transition(medial_neutral, medial_front, CamEvent.FORWARD_SHIFT)
        self.sm_medial.add_transition(medial_front, medial_neutral, CamEvent.BACKWARD_SHIFT)
        self.sm_medial.add_transition(medial_neutral, medial_back, CamEvent.BACKWARD_SHIFT)
        self.sm_medial.add_transition(medial_back, medial_neutral, CamEvent.FORWARD_SHIFT)

        # lateral translation state machine
        lateral_neutral = SCamLateralNeutral(self._rel_direction)
        lateral_right = SCamLateralRight(self._rel_direction)
        lateral_left = SCamLateralLeft(self._rel_direction)
        self.sm_lateral = StateMachine([lateral_neutral, lateral_left, lateral_right])
        self.sm_lateral.add_transition(lateral_neutral, lateral_left, CamEvent.LEFT_SHIFT)
        self.sm_lateral.add_transition(lateral_left, lateral_neutral, CamEvent.RIGHT_SHIFT)
        self.sm_lateral.add_transition(lateral_neutral, lateral_right, CamEvent.RIGHT_SHIFT)
        self.sm_lateral.add_transition(lateral_right, lateral_neutral, CamEvent.LEFT_SHIFT)

        # vertical translation state machine
        vertical_neutral = SCamVerticalNeutral(self._rel_direction)
        vertical_up = SCamVerticalUp(self._rel_direction)
        vertical_down = SCamVerticalDown(self._rel_direction)
        self.sm_vertical = StateMachine([vertical_neutral, vertical_up, vertical_down])
        self.sm_vertical.add_transition(vertical_neutral, vertical_up, CamEvent.UP_SHIFT)
        self.sm_vertical.add_transition(vertical_up, vertical_neutral, CamEvent.DOWN_SHIFT)
        self.sm_vertical.add_transition(vertical_neutral, vertical_down, CamEvent.DOWN_SHIFT)
        self.sm_vertical.add_transition(vertical_down, vertical_neutral, CamEvent.UP_SHIFT)

    def translate_event(self, event: CamEvent) -> None:
        """Processes translation events using state machines.

        Args:
            event: The event to broadcast accross state machines.
        """
        self.sm_lateral.trigger(event)
        self.sm_medial.trigger(event)
        self.sm_vertical.trigger(event)

    def rotate_event(self, mouse_motion: tuple[int, int]) -> None:
        """Reevaluates the camera's orientation based on mouse motion.

        Args:
            mouse_motion: Mouse motion in (x, y) since the last frame.
        """
        self.camera.rotate(-self.look_sens*Vector3(mouse_motion[0], mouse_motion[1], 0))

    def update(self) -> None:
        """Reevaluates the camera's rectilinear velocity."""
        self.sm_medial.update()
        self.sm_lateral.update()
        self.sm_vertical.update()
        if self._rel_direction.length() == 0:
            self.camera.rectilinear_velocity = Vector3(0, 0, 0)
        else:
            rel_vel = self.speed * self._rel_direction.normalize()
            self.camera.rectilinear_velocity =  (rel_vel.x*self.camera.orientation
                + rel_vel.y*self.camera.image_x + rel_vel.z*self.camera.image_y)


class SCam(State):
    """State related to the `Camera` class.

    Methods:
        enter()
        update()
        exit()
    """

    def __init__(self, rel_direction: Vector3) -> None:
        """Creates an instance with access to the camera's relative velocity direction.

        Args:
            rel_direction: The direction in which the camera travels relative to its own 
                orientation: x (medial), y (lateral), z (vertical).
        """
        super().__init__()
        self._rel_direction = rel_direction

    def enter(self) -> None:
        pass

    def update(self) -> None:
        pass

    def exit(self) -> None:
        pass


# medial translation
class SCamMedialFront(SCam):
    def enter(self) -> None:
        self._rel_direction.x = 1


class SCamMedialBack(SCam):
    def enter(self) -> None:
        self._rel_direction.x = -1


class SCamMedialNeutral(SCam):
    def enter(self) -> None:
        self._rel_direction.x = 0


# lateral translation
class SCamLateralRight(SCam):
    def enter(self) -> None:
        self._rel_direction.y = 1


class SCamLateralLeft(SCam):
    def enter(self) -> None:
        self._rel_direction.y = -1


class SCamLateralNeutral(SCam):
    def enter(self) -> None:
        self._rel_direction.y = 0


# vertical translation
class SCamVerticalUp(SCam):
    def enter(self) -> None:
        self._rel_direction.z = 1


class SCamVerticalDown(SCam):
    def enter(self) -> None:
        self._rel_direction.z = -1


class SCamVerticalNeutral(SCam):
    def enter(self) -> None:
        self._rel_direction.z = 0

