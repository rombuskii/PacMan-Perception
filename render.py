import pygame
import numpy as np
from config import *

class Renderer:
    def __init__(self):
        # Initialize pygame and surfaces
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.distance_map_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Sound effect variables
        self.sound_effect_center = (0, 0)
        self.sound_effect_duration = 0
    
    def clear_screen(self):
        """Clear the screen with background color."""
        self.screen.fill(BG_COLOR)
    
    def draw_grid(self, game_map):
        """Draw the game map grid with walls and collectible points."""
        # Draw map elements
        for i in range(game_map.occupancy_map.shape[0]):
            for j in range(game_map.occupancy_map.shape[1]):
                rect = pygame.Rect(j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                # Draw based on cell type
                cell_value = game_map.occupancy_map[i, j]
                if cell_value == -1:  # Wall
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                elif cell_value == 1:  # Regular pellet
                    pygame.draw.circle(self.screen, POINT_COLOR, rect.center, GRID_SIZE // 4)
                elif cell_value == 2:  # Power pellet
                    self._draw_power_pellet(rect.center)
                elif cell_value == 3:  # Sound pellet
                    self._draw_sound_pellet(rect.center)
        
        # Draw active sound effect if any
        self._draw_sound_effect()
    
    def _draw_sound_pellet(self, center):
        """Draw a sound pellet with pulsing effect."""
        # Base circle
        pygame.draw.circle(self.screen, SOUND_PALLET_COLOR, center, GRID_SIZE // 3)
        
        # Pulsing outer circle
        pulse_size = int(GRID_SIZE // 4 + (GRID_SIZE // 8) * (pygame.time.get_ticks() % 1000) / 1000)
        pygame.draw.circle(self.screen, SOUND_PALLET_COLOR, center, pulse_size, 2)
    
    def _draw_sound_effect(self):
        """Draw ripple effect for sound collection."""
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
    
    def draw_distance_map(self, distance_map):
        """Draw the distance map visualization overlay."""
        if distance_map is None:
            return
        
        # Clear the distance map surface
        self.distance_map_surface.fill((0, 0, 0, 0))
        
        # Find the max distance for normalization (excluding infinity)
        max_distance = 0
        for row in distance_map:
            for dist in row:
                if dist != float('inf') and dist > max_distance:
                    max_distance = dist
        
        if max_distance == 0:
            return
        
        # Draw each cell with appropriate coloring
        for i, row in enumerate(distance_map):
            for j, dist in enumerate(row):
                rect = pygame.Rect(j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                if dist != float('inf'):
                    # Draw reachable cell with distance-based color
                    self._draw_distance_cell(rect, dist, max_distance)
                else:
                    # Draw unreachable cell (wall)
                    self._draw_wall_cell(rect)
        
        # Add the visualization to the screen
        self.screen.blit(self.distance_map_surface, (0, 0))
        
        # Add a legend for the distance map
        font = pygame.font.SysFont(None, 24)
        legend = font.render("Distance Map: ON (Press 'D' to toggle)", True, (255, 255, 255))
        self.screen.blit(legend, (10, HEIGHT - 30))
    
    def _draw_distance_cell(self, rect, distance, max_distance):
        """Draw a cell with distance information."""
        norm_dist = distance / max_distance
        
        r = int(DISTANCE_MAP_COLOR_MIN[0] + (DISTANCE_MAP_COLOR_MAX[0] - DISTANCE_MAP_COLOR_MIN[0]) * norm_dist)
        g = int(DISTANCE_MAP_COLOR_MIN[1] + (DISTANCE_MAP_COLOR_MAX[1] - DISTANCE_MAP_COLOR_MIN[1]) * norm_dist)
        b = int(DISTANCE_MAP_COLOR_MIN[2] + (DISTANCE_MAP_COLOR_MAX[2] - DISTANCE_MAP_COLOR_MIN[2]) * norm_dist)
        
        pygame.draw.rect(self.distance_map_surface, (r, g, b, DISTANCE_MAP_OPACITY), rect)
        font = pygame.font.SysFont(None, 16)
        text = font.render(str(int(distance)), True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        self.distance_map_surface.blit(text, text_rect)
    
    def _draw_wall_cell(self, rect):
        """Draw a wall cell in the distance map."""
        # Dark red background for unreachable cells
        pygame.draw.rect(self.distance_map_surface, (80, 0, 0, 100), rect)
        
        # X marking for walls
        pygame.draw.line(self.distance_map_surface, (255, 0, 0, 180), 
                        rect.topleft, rect.bottomright, 2)
        pygame.draw.line(self.distance_map_surface, (255, 0, 0, 180), 
                        rect.bottomleft, rect.topright, 2)
    
    def start_sound_effect(self, x, y):
        """Start a sound ripple effect at the given position."""
        self.sound_effect_center = (y * GRID_SIZE + GRID_SIZE // 2, x * GRID_SIZE + GRID_SIZE // 2)
        self.sound_effect_duration = 420  # running for 7 seconds
    
    def draw_player(self, player):
        """Draw the player at its current position."""
        rect = pygame.Rect(player.position[1] * GRID_SIZE, player.position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, PLAYER_COLOR, rect)
    
    def draw_enemies(self, enemies):
        """Draw all enemies at their current positions."""
        # Get current time in milliseconds to determine color
        current_time = pygame.time.get_ticks()
        
        for enemy in enemies:
            rect = pygame.Rect(enemy.position[1] * GRID_SIZE, enemy.position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # enemy changes color according to mode
            if enemy.ai.current_mode == "chase":
                color = ENEMY_CHASE_COLOR_1 if (current_time // 500) % 2 == 0 else ENEMY_CHASE_COLOR_2
            elif enemy.ai.current_mode == "run away":
                color = ENEMY_RUNAWAY_COLOR
            elif enemy.ai.current_mode == "investigate_sound":
                color = SOUND_PALLET_COLOR
            else:
                color = ENEMY_COLOR
                
            pygame.draw.rect(self.screen, color, rect)
    
    def draw_enemy_vision(self, game_map, enemy_vision_data):
        """Draw enemy vision lines along rows and columns."""
        vision_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        for enemy_data in enemy_vision_data:
            enemy_row, enemy_col = enemy_data['position']
            player_in_sight = enemy_data['player_in_sight']
            mode = enemy_data.get('mode', None)
            
            # Skip drawing vision if enemy is in "run away" mode
            if mode == "run away":
                continue
                
            vision_color = VISION_WARNING_COLOR if player_in_sight else VISION_COLOR
            
            # Draw vision in all four directions
            directions = [
                (0, -1, 0, enemy_col),  # Left
                (0, 1, 0, enemy_col),   # Right
                (-1, 0, enemy_row, 0),  # Up
                (1, 0, enemy_row, 0)    # Down
            ]
            
            for dr, dc, base_row, base_col in directions:
                self._draw_vision_line(vision_surface, game_map, enemy_row, enemy_col, dr, dc, vision_color)
    
        # Add vision overlay to screen
        self.screen.blit(vision_surface, (0, 0))

    def _draw_vision_line(self, surface, game_map, enemy_row, enemy_col, dr, dc, color):
        """Draw a line of sight in a specific direction, stopping at walls."""
        # Start from the position next to the enemy
        curr_row, curr_col = enemy_row + dr, enemy_col + dc
        
        # Continue until hitting a wall or the edge of the map
        while (0 <= curr_row < game_map.occupancy_map.shape[0] and 
            0 <= curr_col < game_map.occupancy_map.shape[1]):
            
            # Stop at walls
            if game_map.occupancy_map[curr_row, curr_col] == -1:
                break
                
            # Draw vision tile
            rect = pygame.Rect(curr_col * GRID_SIZE, curr_row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            
            # Move to next position in this direction
            curr_row += dr
            curr_col += dc
    
    def _draw_power_pellet(self, center):
        """Draw a power pellet with pulsing effect."""
        # Create pulsing effect with time
        current_time = pygame.time.get_ticks()
        pulsing_factor = 0.8 + 0.4 * abs(((current_time % 1000) / 500) - 1)
        
        base_size = GRID_SIZE // 3
        pulse_size = int(base_size * pulsing_factor)
        
        # Draw inner circle and outer ring
        pygame.draw.circle(self.screen, POWER_PELLET_COLOR, center, pulse_size)
        outer_size = pulse_size + 3
        pygame.draw.circle(self.screen, POWER_PELLET_COLOR, center, outer_size, 2)
    
    def render(self, game_map, entity_manager, show_distance_map=False, distance_map=None):
        """Render the complete game state."""
        # Draw basic elements
        self.clear_screen()
        self.draw_grid(game_map)
        
        # Get and draw enemy vision
        enemy_vision_data = entity_manager.get_enemy_vision_data()
        self.draw_enemy_vision(game_map, enemy_vision_data)
        
        # Draw distance map if enabled
        if show_distance_map and distance_map is not None:
            self.draw_distance_map(distance_map)
        
        # Draw entities
        self.draw_player(entity_manager.player)
        self.draw_enemies(entity_manager.enemies)
        
        # Add status message if distance map is on
        if show_distance_map:
            font = pygame.font.SysFont(None, 24)
            status = font.render("Distance Map: ON", True, (255, 255, 255))
            self.screen.blit(status, (10, 10))
        
        # Update display
        pygame.display.flip() 