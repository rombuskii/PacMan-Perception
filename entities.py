import random
from config import ROWS, COLS, DIRECTIONS
from enemy_ai import EnemyAI

class Player:
    def __init__(self, x=1, y=1):
        self.position = [x, y]
        self.current_direction = None
        self.intended_direction = None  # Store the last pressed key direction
        self.renderer = None  # Will be set by EntityManager
    
    # Move player in the given direction if valid
    def move(self, direction, game_map):
        # Try intended direction first, then current direction
        for test_direction in [self.intended_direction, direction]:
            if test_direction:
                new_x = self.position[0] + test_direction[1]
                new_y = self.position[1] + test_direction[0]
                
                if game_map.is_valid_move(new_x, new_y):
                    self.position = [new_x, new_y]
                    self.current_direction = test_direction if test_direction == self.intended_direction else direction
                    collected, is_power, is_sound = game_map.collect_point(new_x, new_y)
                    if collected and is_sound and self.renderer:
                        self.renderer.start_sound_effect(new_x, new_y)
                    return True
        return False

class Enemy:
    def __init__(self, x=None, y=None):
        self.position = [x, y]
        self.ai = EnemyAI()  # Use the AI system
    
    # Move enemy in a random valid direction
    def move(self, game_map, player_position=None):
        # If player position is provided, use AI to decide movement
        if player_position is not None:
            # Update AI mode based on perception
            self.ai.update_mode(self.position, player_position, game_map)
            
            # Get movement direction from AI
            direction = self.ai.decide_move(self.position, player_position, game_map)
            # Add fallback if AI returns None
            if direction is None:
                direction = random.choice(list(DIRECTIONS.values()))
        else:
            # Fallback to random movement if no player position
            direction = random.choice(list(DIRECTIONS.values()))
        
        # Apply the move
        new_x = self.position[0] + direction[1]
        new_y = self.position[1] + direction[0]
        
        if game_map.is_valid_move(new_x, new_y):
            self.position = [new_x, new_y]
            return True
        return False

class EntityManager:
    def __init__(self, game_map, num_enemies=1):
        self.player = Player()
        self.enemies = []
        self.game_map = game_map
        self.renderer = None  # Will be set by Game class
        
        # Initialize player position on the map
        self.game_map.set_position_empty(self.player.position[0], self.player.position[1])
    
    # This function allows entity manager to use renderer to trigger sound effect animations
    def set_renderer(self, renderer):
        self.renderer = renderer
        self.player.renderer = renderer
    
    # Move the player in the given direction
    def move_player(self, direction):
        pass  # We can either remove this method or keep it empty for now
    
    def add_enemy(self, x, y):
        self.enemies.append(Enemy(x, y))
    
    # Move player in current direction if set
    def continue_player_movement(self):
        if self.player.current_direction:
            # Try to move using the current direction
            self.player.move(self.player.current_direction, self.game_map)
    
    # Move all enemies
    def move_enemies(self):
        player_pos = self.player.position
        
        for enemy in self.enemies:
            enemy.move(self.game_map, player_pos)
    
    # Check if player collided with any enemy
    def check_collision(self):
        for enemy in self.enemies:
            if enemy.position == self.player.position:
                return True
        return False 