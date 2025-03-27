import pygame
from config import WIDTH, HEIGHT, GRID_SIZE, PLAYER_COLOR, ENEMY_COLOR, WALL_COLOR, POINT_COLOR, SOUND_PALLET_COLOR, BG_COLOR

class Renderer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.sound_effect_radius = 0
        self.sound_effect_duration = 0
    
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
                
                # Draw sound pallets
                elif game_map.occupancy_map[i, j] == 3:
                    pygame.draw.circle(self.screen, SOUND_PALLET_COLOR, rect.center, GRID_SIZE // 3)
                    pulse_size = int(GRID_SIZE // 4 + (GRID_SIZE // 8) * (pygame.time.get_ticks() % 1000) / 1000)
                    pygame.draw.circle(self.screen, SOUND_PALLET_COLOR, rect.center, pulse_size, 2)
        
        # Draw sound effect if active
        if self.sound_effect_duration > 0:
            self.sound_effect_duration -= 1
            base_radius = GRID_SIZE * 2
            ripple_speed = 0.5  
            time_passed = 420 - self.sound_effect_duration  
            current_radius = (time_passed * ripple_speed) % base_radius
            
            # Draw multiple circles to represent the sound effect
            for i in range(3):
                radius = (current_radius + i * (base_radius // 3)) % base_radius
                pygame.draw.circle(self.screen, SOUND_PALLET_COLOR, self.sound_effect_center, radius, 2)
    
    def start_sound_effect(self, x, y):
        self.sound_effect_center = (y * GRID_SIZE + GRID_SIZE // 2, x * GRID_SIZE + GRID_SIZE // 2)
        self.sound_effect_duration = 420  # running for 7 seconds
    
    # Draw the player at its current position
    def draw_player(self, player):
        rect = pygame.Rect(player.position[1] * GRID_SIZE, player.position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, PLAYER_COLOR, rect)
    
    # Draw all enemies at their current positions
    def draw_enemies(self, enemies):
        for enemy in enemies:
            rect = pygame.Rect(enemy.position[1] * GRID_SIZE, enemy.position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, ENEMY_COLOR, rect)
    
    # Render the complete game state
    def render(self, game_map, entity_manager):
        self.clear_screen()
        self.draw_grid(game_map)
        self.draw_player(entity_manager.player)
        self.draw_enemies(entity_manager.enemies)
        pygame.display.flip() 