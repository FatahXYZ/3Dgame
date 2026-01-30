"""
Game Configuration Module
Contains all game settings and constants for the 3D platformer.
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "3D Platformer Game"
TARGET_FPS = 60

# Player settings
PLAYER_SIZE = 1.0  # Size of the player cube
PLAYER_SPEED = 5.0  # Movement speed units per second
PLAYER_JUMP_FORCE = 10.0  # Initial jump velocity
PLAYER_START_POS = [0.0, 2.0, 0.0]  # Starting position [x, y, z]

# Physics settings
GRAVITY = -20.0  # Gravity acceleration (negative pulls down)
COLLISION_Y_TOLERANCE_ABOVE = 0.1  # Tolerance for landing on platform (above)
COLLISION_Y_TOLERANCE_BELOW = 0.5  # Tolerance for landing on platform (below)

# Camera settings
CAMERA_DISTANCE = 10.0  # Distance from player
CAMERA_HEIGHT = 5.0  # Height above player
CAMERA_SMOOTHING = 0.1  # Camera follow smoothing (0-1, lower = smoother)

# Platform colors (RGB normalized 0-1)
PLATFORM_COLOR = (0.5, 0.5, 0.5)  # Gray
PLAYER_COLOR = (0.0, 0.6, 1.0)  # Blue
GOAL_COLOR = (1.0, 0.8, 0.0)  # Gold

# Game objects
PLATFORMS = [
    # Starting platform: [x, y, z, width, height, depth]
    {"pos": [0, 0, 0], "size": [6, 0.5, 6]},
    # Jump platforms
    {"pos": [8, 2, 0], "size": [4, 0.5, 4]},
    {"pos": [15, 4, 0], "size": [4, 0.5, 4]},
    {"pos": [22, 6, 3], "size": [5, 0.5, 5]},
    # Final platform with goal
    {"pos": [30, 8, 0], "size": [6, 0.5, 6]},
]

# Goal position (where player needs to reach)
GOAL_POSITION = [30, 9, 0]
GOAL_SIZE = 1.5
