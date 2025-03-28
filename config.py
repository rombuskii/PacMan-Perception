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
FPS = 60  # Frames per second for smooth rendering
GAME_SPEED = 5  # Game logic updates per second (adjust this for desired game speed)