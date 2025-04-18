import pygame

# Game dimensions
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 20
ROWS, COLS = 33, 31

# Colors
PLAYER_COLOR = (255, 255, 0)  
ENEMY_COLOR = (255, 0, 0)     
ENEMY_CHASE_COLOR_1 = (255, 0, 0)     
ENEMY_CHASE_COLOR_2 = (0, 0, 255)     
WALL_COLOR = (75, 0, 130)        
POINT_COLOR = (0, 255, 0)     
SOUND_PALLET_COLOR = (255, 165, 0)  
ENEMY_INVESTIGATE_COLOR = (255, 165, 0) 
BG_COLOR = (0, 0, 0)          
POWER_PELLET_COLOR = (0, 191, 255)  
ENEMY_RUNAWAY_COLOR = (255, 255, 255) 

VISION_COLOR = (255, 0, 0, 70) 
VISION_WARNING_COLOR = (255, 0, 0, 170) 

# Distance map visualization
DISTANCE_MAP_VISIBLE = False
DISTANCE_MAP_COLOR_MIN = (0, 0, 100) 
DISTANCE_MAP_COLOR_MAX = (255, 0, 255)  
DISTANCE_MAP_OPACITY = 150 

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
ENEMY_SPEED_FACTOR = 1.1
CHASE_DURATION = 3
POWER_PELLET_DURATION = 100 