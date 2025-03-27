class EnemyPerception:
    def __init__(self):
        self.perception_range = 10  # Default perception range
    
    def can_see_player(self, enemy_position, player_position, game_map):
        pass
        

class EnemyAI:
    def __init__(self):
        self.perception = EnemyPerception()
        self.current_mode = "patrol"  # patrol, seekSoundSource, runAway
        self.patrol_direction = [0, 1]  # Initialize with a default direction
        self.is_horizontal = True  # Track if moving horizontally or vertically
    
    def decide_move(self, enemy_position, player_position, game_map):
        if self.current_mode == "patrol":
            return self.patrol(enemy_position, game_map)
    
    # This function represents the enemy's patrol mode
    # The enemy will move in a straight line until it hits a wall, then it will change direction
    def patrol(self, enemy_position, game_map):
        # Try to move in current direction
        new_x = enemy_position[0] + self.patrol_direction[1]
        new_y = enemy_position[1] + self.patrol_direction[0]
        
        # If current move is valid, keep going in same direction
        if game_map.is_valid_move(new_x, new_y):
            return self.patrol_direction
            
        # If we hit a wall, change direction
        if self.is_horizontal:
            # If moving horizontally (left/right), reverse direction
            self.patrol_direction[1] *= -1
            
            # If still can't move, switch to vertical movement
            new_x = enemy_position[0] + self.patrol_direction[1]
            new_y = enemy_position[1] + self.patrol_direction[0]
            if not game_map.is_valid_move(new_x, new_y):
                self.is_horizontal = False
                self.patrol_direction = [1, 0]  # Start moving down
        else:
            # If moving vertically (up/down), reverse direction
            self.patrol_direction[0] *= -1
            
            # If still can't move, switch to horizontal movement
            new_x = enemy_position[0] + self.patrol_direction[1]
            new_y = enemy_position[1] + self.patrol_direction[0]
            if not game_map.is_valid_move(new_x, new_y):
                self.is_horizontal = True
                self.patrol_direction = [0, 1]
        return self.patrol_direction
    
    def calculate_path(self, start_position, target_position, game_map):
        pass
    
    # There will be three modes: patrol, chase, run away
    # If Player pick up the red pellet, the pellet will make sound, and the enemy will chase the player
    # If Player pick up the power pellet, the enemy will run away from the player because they can die.
    def update_mode(self, enemy_position, player_position, game_map):
        pass
