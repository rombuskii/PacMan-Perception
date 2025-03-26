import random
from config import ROWS, COLS, DIRECTIONS
from enemy_ai import EnemyAI

class Player:
    def __init__(self, x=1, y=1):
        self.position = [x, y]
        self.current_direction = None
    
    # Move player in the given direction if valid
    def move(self, direction, game_map):
        new_x = self.position[0] + direction[1]
        new_y = self.position[1] + direction[0]
        
        if game_map.is_valid_move(new_x, new_y):
            self.position = [new_x, new_y]
            game_map.collect_point(new_x, new_y)
            return True
        return False

class Enemy:
    def __init__(self, x=None, y=None):
        # Default to bottom right if not specified
        self.position = [x if x is not None else ROWS - 17, 
                        y if y is not None else COLS - 17]
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
        
        # Initialize player position on the map
        self.game_map.set_position_empty(self.player.position[0], self.player.position[1])
        
        # Create enemies
        for _ in range(num_enemies):
            self.enemies.append(Enemy())
    
    # Move the player in the given direction
    def move_player(self, direction):
        return self.player.move(direction, self.game_map)
    
    # Move player in current direction if set
    def continue_player_movement(self):
        if self.player.current_direction:
            # Try to move in current direction
            if not self.player.move(self.player.current_direction, self.game_map):
                # If movement failed (hit a wall), we keep the current_direction
                pass
    
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