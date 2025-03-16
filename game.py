import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
PLAYER_COLOR = (255, 255, 0)
ENEMY_COLOR = (255, 0, 0)
WALL_COLOR = (0, 0, 255)
POINT_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)

# Directions
DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with Occupancy Map")

# Generate a simple map with walls and points
occupancy_map = np.zeros((ROWS, COLS))
for i in range(ROWS):
    for j in range(COLS):
        if random.random() < 0.1:
            occupancy_map[i, j] = -1  # Wall
        else:
            occupancy_map[i, j] = 1  # Collectible point

# Player and enemy positions
player_pos = [1, 1]
enemies = [[ROWS - 2, COLS - 2]]
occupancy_map[player_pos[0], player_pos[1]] = 0  # No point on player start

def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if occupancy_map[i, j] == -1:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif occupancy_map[i, j] == 1:
                pygame.draw.circle(screen, POINT_COLOR, rect.center, GRID_SIZE // 4)

def move_player(direction):
    global player_pos
    new_x = player_pos[0] + direction[1]
    new_y = player_pos[1] + direction[0]
    if 0 <= new_x < ROWS and 0 <= new_y < COLS and occupancy_map[new_x, new_y] != -1:
        player_pos = [new_x, new_y]
        occupancy_map[new_x, new_y] = 0  # Remove collected point

def move_enemies():
    for enemy in enemies:
        direction = random.choice(list(DIRECTIONS.values()))
        new_x, new_y = enemy[0] + direction[1], enemy[1] + direction[0]
        if 0 <= new_x < ROWS and 0 <= new_y < COLS and occupancy_map[new_x, new_y] != -1:
            enemy[0], enemy[1] = new_x, new_y

def check_collision():
    for enemy in enemies:
        if enemy == player_pos:
            return True
    return False

def check_win():
    return np.sum(occupancy_map == 1) == 0

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_grid()
    
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[1] * GRID_SIZE, player_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy[1] * GRID_SIZE, enemy[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key in DIRECTIONS:
            move_player(DIRECTIONS[event.key])
    
    move_enemies()
    
    if check_collision():
        print("Game Over! You were caught.")
        running = False
    
    if check_win():
        print("Congratulations! You collected all points.")
        running = False
    
    pygame.time.delay(200)

pygame.quit()
