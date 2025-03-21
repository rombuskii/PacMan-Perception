import pygame
from config import WIDTH, HEIGHT, GRID_SIZE, PLAYER_COLOR, ENEMY_COLOR, WALL_COLOR, POINT_COLOR, BG_COLOR

class Renderer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Clear the screen with background color
    def clear_screen(self):
        self.screen.fill(BG_COLOR)
    
    # Draw the game map grid with walls and collectible points
    def draw_grid(self, game_map):
        for i in range(game_map.occupancy_map.shape[0]):
            for j in range(game_map.occupancy_map.shape[1]):
                rect = pygame.Rect(j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                # Draw walls
                if game_map.occupancy_map[i, j] == -1:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                
                # Draw collectible points
                elif game_map.occupancy_map[i, j] == 1:
                    pygame.draw.circle(self.screen, POINT_COLOR, rect.center, GRID_SIZE // 4)
    
    # Draw the player at its current position
    def draw_player(self, player):
        rect = pygame.Rect(
            player.position[1] * GRID_SIZE, 
            player.position[0] * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        pygame.draw.rect(self.screen, PLAYER_COLOR, rect)
    
    # Draw all enemies at their current positions
    def draw_enemies(self, enemies):
        for enemy in enemies:
            rect = pygame.Rect(
                enemy.position[1] * GRID_SIZE,
                enemy.position[0] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(self.screen, ENEMY_COLOR, rect)
    
    # Render the complete game state
    def render(self, game_map, entity_manager):
        self.clear_screen()
        self.draw_grid(game_map)
        self.draw_player(entity_manager.player)
        self.draw_enemies(entity_manager.enemies)
        pygame.display.flip() 