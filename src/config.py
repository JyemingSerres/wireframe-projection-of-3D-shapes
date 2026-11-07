"""Contains the program's configurations and other constants.
"""

import math
from enum import Enum

__author__ = "Jye-Ming Serres"


# Display settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
TARGET_FRAME_RATE = 100

# Camera controls
CAMERA_LOOK_SENS = 0.1
CAMERA_SPEED = 2000 # distance units per second

# Math constants
GOLDEN_RATIO = (1 + math.sqrt(5))/2

# Colors
class Color(Enum):
    WHITE = (255, 255,255),
    RED = (255, 0, 0),
    GREEN = (0, 255, 0),
    BLUE = (0, 0, 255),
    YELLOW = (255, 255, 0),
    MAGENTA = (255, 0, 255),
    CYAN = (0, 255, 255),
    DEEP_SPACE = (10, 10, 20),
