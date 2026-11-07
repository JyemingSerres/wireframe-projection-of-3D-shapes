#!/usr/bin/env python3
"""A showcase of perspective projection.

This program creates a simulation containing five platonic solids of different colors and displays 
them in a window.
"""

import sys

import pygame
from pygame import Vector3

from config import Color, SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FRAME_RATE
from utils import resource_path
from shape_factory import ShapeFactory
from camera import Camera
from world import World
from display import Display
from engine import Engine

__author__ = "Jye-Ming Serres"


if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED, vsync=1)
    icon = pygame.image.load(resource_path("assets/icon.png"))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Wireframe projection of 3D shapes")

    # Initialize the program
    shape_factory = ShapeFactory()
    tetrahedron = shape_factory.make_shape("tetrahedron", Vector3(600, -600, 0), 100, Color.RED)
    cube = shape_factory.make_shape("cube", Vector3(600, -300, 0), 100, Color.BLUE)
    octahedron = shape_factory.make_shape("octahedron", Vector3(600, 0, 0), 100, Color.GREEN)
    dodecahedron = shape_factory.make_shape("dodecahedron", Vector3(600, 300, 0), 100, Color.YELLOW)
    icosahedron = shape_factory.make_shape("icosahedron", Vector3(600, 600, 0), 100, Color.CYAN)

    camera = Camera(Vector3(-200, 0, 25), 360)
    world = World(camera, [tetrahedron, cube, octahedron, dodecahedron, icosahedron])
    display = Display(screen)
    engine = Engine(world, display, clock)

    while engine.running:
        clock.tick(TARGET_FRAME_RATE) # Try to reach the target frame rate if vsync request is denied.
        engine.handle_events()
        engine.update_world()
        engine.render()

    pygame.quit()
    sys.exit()
