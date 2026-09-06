"""Provides the view of the program.

Classes:
    Display
"""

import pygame
from pygame import Vector3, Vector2, draw
from pygame.surface import Surface

from config import Color
from world import World
from shape import Shape

__author__ = "Jye-Ming Serres"


class Display:
    """Manages everything related to the final display. Acts as the view of the program.

    Methods:
        draw()
    """

    def __init__(self, screen: Surface) -> None:
        """Creates an instance from a surface.

        Args:
            screen: The surface to draw on.
        """
        self._screen = screen
        self._screen_center = Vector2(screen.get_width(), screen.get_height())/2
        self._font = pygame.font.SysFont("Verdana", 12)
        self._crosshair_size = 10
        self._background_color = Color.DEEP_SPACE
        self._ui_color = Color.WHITE
        self._ui_margin = 5

    def draw(self, world: World, fps: float) -> None:
        """Clears the last frame and draws a new view of the simulation and the UI on top.

        Args:
            world: Model of the simulation.
            fps: Frames/second of the program.
        """
        self._screen.fill(self._background_color.value)
        self._draw_world(world)
        self._draw_ui(fps, world.camera.aperture)

    def _draw_world(self, world: World) -> None:
        """Draws a view of the simulation using the pinhole camera model. For more information:
            https://en.wikipedia.org/wiki/Pinhole_camera_model

        Args:
            world: Model of the simulation.
        """
        camera = world.camera
        shapes = world.shapes

        # Sort shapes by the distance of their center to the image plane. We make sure to draw
        # shapes that are closer on top of shapes that are further.

        def center_to_plane_dist(shape: Shape):
            return (shape.center - camera.aperture).dot(camera.orientation)
        shapes.sort(key=center_to_plane_dist, reverse=True)

        for shape in shapes:
            vertices_screen = []
            within_frame = True

            for vertex in shape.vertices:

                # We find the vertex's distance to the image plane with its orthogonal projection
                # onto the camera's orientation. Since the orientation vector is normalized,
                # the projection can be simplified to a dot product and the vector part is ommited.

                vrtx_rel = vertex - camera.aperture
                vrtx_dist = vrtx_rel.dot(camera.orientation)

                if vrtx_dist > 0: # vertex needs to be strictly in front of the aperture

                    # We scale the vertex' coordinates based its distance to the image plane
                    # according to the pinhole camera model. We calculate the vertex's (x, y)
                    # position on the image plane relative to the image center with two orthogonal
                    # projections (refer to the previous paragraph for why a simple dot product is
                    # used). Finally, we convert (x, y) to coordinates matching pygame's interface.

                    vrtx_rel_scaled = vrtx_rel*camera.focal_length/vrtx_dist
                    vrtx_x = vrtx_rel_scaled.dot(camera.image_x)
                    vrtx_y = vrtx_rel_scaled.dot(camera.image_y)
                    vrtx_screen = Vector2(vrtx_x, -vrtx_y) + self._screen_center

                    vertices_screen.append(vrtx_screen)
                else:
                    within_frame = False
                    break

            if within_frame:
                for edge in shape.edges:
                    draw.aaline(self._screen, shape.color.value,
                        vertices_screen[edge[0]], vertices_screen[edge[1]])

    def _draw_ui(self, fps: float, camera_pos: Vector3) -> None:
        """Draws the keyboard controls, the position of the end user, the fps of the program and a 
            crosshair.

        Args:
            fps: Frames/second of the program.
            camera_pos: Current (x, y, z) position of the end user (camera).
        """
        # draw crosshair
        x = self._screen_center.x
        y = self._screen_center.y
        offset = self._crosshair_size/2
        draw.line(self._screen, self._ui_color.value, (x - offset, y), (x + offset, y))
        draw.line(self._screen, self._ui_color.value, (x, y - offset), (x, y + offset))

        # draw texts
        str_controls = """[ESC] quit
            [W] forward
            [A] left
            [S] backward
            [D] right
            [LSHIFT] down
            [SPACE] up"""
        str_fps = f"FPS: {round(fps, 1)}"
        str_pos = f"({camera_pos.x:.1f}, {camera_pos.y:.1f}, {camera_pos.z:.1f})"

        height = self._screen.get_height()
        width = self._screen.get_width()
        self._blit_lines(str_controls, (self._ui_margin, self._ui_margin), line_spacing=2)
        self._blit_line(str_fps, (self._ui_margin, height - self._ui_margin), b_just=True)
        self._blit_line(str_pos, (width - self._ui_margin, self._ui_margin), r_just=True)

    def _blit_line(
            self,
            string: str,
            coord: tuple[int,  int],
            r_just: bool = False,
            b_just: bool = False) -> None:
        """Draws a single line of text at the specified position.

        Args:
            string: The string to draw. Will be cut when encountering a new line.
            coord: The position onto which the line will justify to.
            r_just: Whether the line should justify on its right.
            b_just: Whether the line should justify on its bottom.
        """
        surface = self._font.render(string.strip(), True, self._ui_color.value)
        x = coord[0] - (surface.get_width() if r_just else 0)
        y = coord[1] - (surface.get_height() if b_just else 0)
        self._screen.blit(surface, (x, y))

    def _blit_lines(
            self,
            string: str,
            coord: tuple[int,  int],
            r_just: bool = False,
            b_just: bool = False,
            line_spacing: int = 0) -> None:
        """Draws multiple lines of text at the specified position.

        Args:
            string: The string to draw.
            coord: The position onto which the lines will justify to.
            r_just: Whether the line should justify on their right.
            b_just: Whether the line should justify on their bottom.
            line_spacing: Number of pixels between each line.
        """
        lines = string.split("\n")

        total_offset = 0
        blits = []
        for line in lines:
            surface = self._font.render(line.strip(), True, self._ui_color.value)
            x = coord[0] - (surface.get_width() if r_just else 0)
            y = coord[1] - (surface.get_height() if b_just else 0) + total_offset
            blits.append((surface, (x, y)))
            offset = surface.get_height() + line_spacing
            total_offset += -offset if b_just else offset

        self._screen.blits(blit_sequence=blits, doreturn=0)
