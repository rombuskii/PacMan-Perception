import pygame

# Game dimensions
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 20
ROWS, COLS = 33, 31

# Colors
PLAYER_COLOR = (255, 255, 0)  # Yellow
ENEMY_COLOR = (255, 0, 0)     # Red
WALL_COLOR = (0, 0, 255)      # Blue
POINT_COLOR = (0, 255, 0)     # Green
SOUND_PALLET_COLOR = (255, 165, 0)  # Orange
BG_COLOR = (0, 0, 0)          # Black

# Enemy vision
VISION_COLOR = (255, 0, 0, 70)  # Semi-transparent red
VISION_WARNING_COLOR = (255, 0, 0, 170)  # Brighter red for player in sight

# Distance map visualization
DISTANCE_MAP_VISIBLE = False  # Toggle for distance map visualization
DISTANCE_MAP_COLOR_MIN = (0, 0, 100)  # Dark blue for minimum distance
DISTANCE_MAP_COLOR_MAX = (255, 0, 255)  # Purple for maximum distance
DISTANCE_MAP_OPACITY = 150  # Alpha value for overlay (0-255)

# Movement directions
DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}

# Game settings
GAME_TITLE = "Pac-Man"
FRAME_DELAY = 250
FPS = 60 
GAME_SPEED = 5 
ENEMY_SPEED_FACTOR = 1.01
CHASE_DURATION = 3