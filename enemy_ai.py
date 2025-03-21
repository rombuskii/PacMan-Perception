class EnemyPerception:
    def __init__(self):
        self.perception_range = 10  # Default perception range
    
    def can_see_player(self, enemy_position, player_position, game_map):
        pass
        

class EnemyAI:
    def __init__(self):
        self.perception = EnemyPerception()
        self.current_mode = "patrol"  # patrol, chase, scatter, etc.
    
    def decide_move(self, enemy_position, player_position, game_map):
        pass
    
    def calculate_path(self, start_position, target_position, game_map):
        pass
    
    # There will be three modes: patrol, chase, run away
    # If Player pick up the red pellet, the pellet will make sound, and the enemy will chase the player
    # If Player pick up the power pellet, the enemy will run away from the player because they can die.
    def update_mode(self, enemy_position, player_position, game_map):
        pass
