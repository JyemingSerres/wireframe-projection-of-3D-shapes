"""Provides the engine/controller of the program.

Classes:
    Engine
"""

import pygame
from pygame.time import Clock

from camera_controller import CameraController, CamEvent
from world import World
from display import Display

__author__ = "Jye-Ming Serres"


class Engine:
    """Acts as the main controller between pygame user inputs, the model and the view.

    Attributes:
        running (`bool`): Indicates if the engine is running.
        world (:obj:`World`): Acts as the model of the simulation.
        display (:obj:`Display`): Manages the view of the simulation and the UI.
        clock (:obj:`pygame.time.Clock`): Tracks time elapsed and main loop frequency.

    Methods:
        handle_events()
        update_world()
        render()
    """

    def __init__(self, world: World, display: Display, clock: Clock) -> None:
        """Creates an instance with passed world, display and clock.

        Args:
            world: Acts as the model of the simulation.
            display: Manages the view of the simulation and the UI.
            clock: Tracks time elapsed and main loop frequency.
        """
        self.running = True
        self.world = world
        self.display = display
        self.clock = clock
        self._cam_control = CameraController(self.world.camera)

        self._focus = True
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.event.set_keyboard_grab(False)

    def handle_events(self) -> None:
        """Handles pygame's event loop and other user inputs through pygame."""
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE: self.running = False
                        case pygame.K_a: self._cam_control.translate_event(CamEvent.LEFT_SHIFT)
                        case pygame.K_d: self._cam_control.translate_event(CamEvent.RIGHT_SHIFT)
                        case pygame.K_s: self._cam_control.translate_event(CamEvent.BACKWARD_SHIFT)
                        case pygame.K_w: self._cam_control.translate_event(CamEvent.FORWARD_SHIFT)
                        case pygame.K_SPACE: self._cam_control.translate_event(CamEvent.UP_SHIFT)
                        case pygame.K_LSHIFT: self._cam_control.translate_event(CamEvent.DOWN_SHIFT)
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_a: self._cam_control.translate_event(CamEvent.RIGHT_SHIFT)
                        case pygame.K_d: self._cam_control.translate_event(CamEvent.LEFT_SHIFT)
                        case pygame.K_s: self._cam_control.translate_event(CamEvent.FORWARD_SHIFT)
                        case pygame.K_w: self._cam_control.translate_event(CamEvent.BACKWARD_SHIFT)
                        case pygame.K_SPACE: self._cam_control.translate_event(CamEvent.DOWN_SHIFT)
                        case pygame.K_LSHIFT: self._cam_control.translate_event(CamEvent.UP_SHIFT)
                case pygame.WINDOWFOCUSLOST:
                    self._focus = False
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                case pygame.WINDOWFOCUSGAINED:
                    self._focus = True
                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)

        mouse_delta = pygame.mouse.get_rel() if self._focus else (0, 0)
        self._cam_control.rotate_event(mouse_delta)

    def update_world(self) -> None:
        """Steps the simulation proportionally to real time elapsed.

        Ideally called after handle_events().
        """
        self._cam_control.update()
        dt = self.clock.get_time() / 1000
        self.world.update(dt)

    def render(self) -> None:
        """Draws the simulation view and the UI then renders them on the screen.

        Should be called after update_world().
        """
        if pygame.display.get_active():
            self.display.draw(self.world, self.clock.get_fps())
            pygame.display.flip()
