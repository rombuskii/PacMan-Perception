import random
from config import *
from enemy_ai import EnemyAI

class Player:
    def __init__(self, x=1, y=1):
        """Initialize player entity with a position and movement state."""
        self.position = [x, y]
        self.current_direction = None
        self.intended_direction = None  # Store the last pressed key direction
        self.renderer = None  # Will be set by EntityManager
        self.entity_manager = None  # Reference to entity manager
    
    def move(self, direction, game_map):
        """Move the player in the given direction if valid."""
        for test_direction in [self.intended_direction, direction]:
            if test_direction:
                new_x = self.position[0] + test_direction[1]
                new_y = self.position[1] + test_direction[0]
                
                if game_map.is_valid_move(new_x, new_y):
                    self.position = [new_x, new_y]
                    self.current_direction = test_direction if test_direction == self.intended_direction else direction                    
                    self._handle_collection(new_x, new_y, game_map)
                    return True
        return False

    # Handle pellet collection and trigger appropriate effects
    def _handle_collection(self, x, y, game_map):
        collected, is_power, is_sound = game_map.collect_point(x, y)
        if collected and is_sound and self.renderer:
            self.renderer.start_sound_effect(x, y)
            # Notify entity manager about sound pellet
            if self.entity_manager:
                self.entity_manager.sound_detected(x, y)

class Enemy:
    def __init__(self, x=None, y=None):
        """Initialize enemy entity with a position and AI controller."""
        self.position = [x, y]
        self.previous_position = [x, y]  # Initialize previous position
        self.ai = EnemyAI()  # AI system for enemy behavior
        self.move_counter = 0  # Counter for movement speed control
        self.next_direction = None  # Store next planned direction

    def move(self, game_map, player_position=None, sound_position=None):
        """
        Move the enemy based on AI or random movement.
        Always updates AI decisions but applies movement at a reduced rate.
        Returns True if movement was successful, False otherwise.
        """    
        self.next_direction = self._get_movement_direction(game_map, player_position, sound_position)
        
        # Only apply movement at reduced speed determined by ENEMY_SPEED_FACTOR
        self.move_counter += 1
        if self.move_counter >= ENEMY_SPEED_FACTOR:
            self.move_counter = 0
            return self._apply_move(self.next_direction, game_map)
        return False
    
    def _get_movement_direction(self, game_map, player_position, sound_position=None):
        """Determine which direction the enemy should move."""
        if player_position is not None:
            # Update AI mode based on perception
            self.ai.update_mode(self.position, player_position, game_map, sound_position)
            
            # Get movement direction from AI
            direction = self.ai.decide_move(self.position, player_position, game_map)
            
            # Fallback to random if AI returns None
            if direction is None:
                direction = random.choice(list(DIRECTIONS.values()))
        else:
            # Random movement if no player position
            direction = random.choice(list(DIRECTIONS.values()))
            
        return direction
    
    def _apply_move(self, direction, game_map):
        """Apply the movement in the given direction if valid."""
        new_x = self.position[0] + direction[1]
        new_y = self.position[1] + direction[0]
        
        if game_map.is_valid_move(new_x, new_y):
            # Store previous position before moving
            self.previous_position = self.position.copy()
            self.position = [new_x, new_y]
            return True
        return False

class EntityManager:
    def __init__(self, game_map, num_enemies=1):
        self.player = Player()
        self.enemies = []
        self.game_map = game_map
        self.renderer = None  # Will be set by Game class
        self.game_map.set_position_empty(self.player.position[0], self.player.position[1]) # Initialize player position on the map
        self.score = 0
        self.sound_position = None
        self.player.entity_manager = self
    
    def set_renderer(self, renderer):
        self.renderer = renderer
        self.player.renderer = renderer
    
    def add_enemy(self, x, y):
        self.enemies.append(Enemy(x, y))
    
    def continue_player_movement(self):
        if self.player.current_direction:
            self.player.move(self.player.current_direction, self.game_map)
    
    def sound_detected(self, x, y):
        """Handle sound pellet detection"""
        self.sound_position = [x, y]
        
        # Find closest enemy not in run away mode
        closest_enemy = None
        min_distance = float('inf')
        
        # Find the closest enemy that is not in run away mode
        for enemy in self.enemies:
            if enemy.ai.current_mode != "run away":
                distance = enemy.ai.perception.calculate_distance(enemy.position, [x, y])
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        # Set closest enemy to investigate
        if closest_enemy:
            closest_enemy.ai.current_mode = "investigate_sound"
            closest_enemy.ai.sound_location = [x, y]
            
            # Clear the sound position so other enemies don't also investigate
            self.sound_position = None
    
    def move_enemies(self):
        player_pos = self.player.position
        
        for enemy in self.enemies:
            # Check if enemy reached sound location
            if enemy.ai.current_mode == "investigate_sound" and enemy.ai.sound_location:
                if enemy.position[0] == enemy.ai.sound_location[0] and enemy.position[1] == enemy.ai.sound_location[1]:
                    enemy.ai.current_mode = "patrol"
                    enemy.ai.sound_location = None
                    
            enemy.move(self.game_map, player_pos, self.sound_position)
    
    def check_collision(self):
        player_pos = self.player.position
        player_prev_pos = [player_pos[0] - (self.player.current_direction[1] if self.player.current_direction else 0),
                           player_pos[1] - (self.player.current_direction[0] if self.player.current_direction else 0)]
        
        enemies_to_remove = []
        collision_occurred = False
        
        for i, enemy in enumerate(self.enemies):
            # Check if player and enemy are in the same position
            position_match = enemy.position == player_pos
            
            # Check if the passed through the enemy
            enemy_prev_pos = getattr(enemy, 'previous_position', None)
            pass_through = False
            if enemy_prev_pos:
                pass_through = enemy.position == player_prev_pos and enemy_prev_pos == player_pos
            
            # If any collision type occurred
            if position_match or pass_through:
                # If enemy is in run away mode, player can eat the enemy
                if enemy.ai.current_mode == "run away":
                    enemies_to_remove.append(i)
                    self.score += 200  # Award points for eating an enemy
                else:
                    collision_occurred = True
        # Remove eaten enemies
        for i in sorted(enemies_to_remove, reverse=True):
            del self.enemies[i]
        
        return collision_occurred
    
    def get_enemy_vision_data(self):
        vision_data = []
        player_pos = self.player.position
        
        for enemy in self.enemies:
            # Get enemy vision data
            enemy_position = enemy.position
            player_in_sight = enemy.ai.perception.can_see_player(enemy_position, player_pos, self.game_map)
            
            vision_data.append({
                'position': enemy_position,
                'player_in_sight': player_in_sight,
                'mode': enemy.ai.current_mode
            })
            
        return vision_data 