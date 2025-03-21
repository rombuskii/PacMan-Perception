import pygame

# Game dimensions
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 20
# Update these values to match the actual map dimensions
ROWS, COLS = 33, 31  # Match the actual size of the pacman_layout

# Colors
PLAYER_COLOR = (255, 255, 0)  # Yellow
ENEMY_COLOR = (255, 0, 0)     # Red
WALL_COLOR = (0, 0, 255)      # Blue
POINT_COLOR = (0, 255, 0)     # Green
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
FRAME_DELAY = 200