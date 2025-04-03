import heapq
import time
from config import CHASE_DURATION

class EnemyPerception:

    def calculate_distance(self, start_position, target_position):
        """Calculate the Manhattan distance between two positions."""
        return abs(start_position[0] - target_position[0]) + abs(start_position[1] - target_position[1])

    def can_see_player(self, enemy_position, player_position, game_map):
        """
        Check if the enemy can see the player by looking in straight lines (horizontal and vertical).
        Stops checking when it hits a wall.
        """
        # Get positions
        enemy_row, enemy_col = enemy_position
        player_row, player_col = player_position
        
        # Check if player is on the same row (horizontal line)
        if enemy_row == player_row:
            # Check if there's a clear horizontal path
            start_col, end_col = min(enemy_col, player_col), max(enemy_col, player_col)
            for check_col in range(int(start_col) + 1, int(end_col)):
                if game_map.occupancy_map[enemy_row, check_col] == -1:  # Wall found
                    return False
            return True
        
        # Check if player is on the same column (vertical line)
        if enemy_col == player_col:
            # Check if there's a clear vertical path
            start_row, end_row = min(enemy_row, player_row), max(enemy_row, player_row)
            for check_row in range(int(start_row) + 1, int(end_row)):
                if game_map.occupancy_map[check_row, enemy_col] == -1:  # Wall found
                    return False
            return True
        
        # Not in the same row or column, so can't see player
        return False

class EnemyAI:
    def __init__(self):
        self.perception = EnemyPerception()
        self.current_mode = "patrol"  # patrol, chase, run away, investigate_sound
        self.patrol_direction = [0, 1]  # Initialize with a default direction
        self.is_horizontal = True  # Track if moving horizontally or vertically
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        self.chase_timer = CHASE_DURATION
        self.last_update_time = 0
        self.sound_location = None  # Store sound pellet location when heard
    
    def update_mode(self, enemy_position, player_position, game_map, sound_position=None, current_time=None):
        """Update the AI mode based on the game state."""
        # If current_time is not provided, get the current time
        if current_time is None:
            current_time = time.time()
        
        # Initialize last_update_time if this is the first update
        if self.last_update_time == 0:
            self.last_update_time = current_time
        
        # Calculate time delta since last update
        dt = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Check if power pellet is active - this takes precedence over other modes
        if game_map.is_power_pellet_active():
            self.current_mode = "run away"
            return
        
        # If we were in run away mode but power pellet is no longer active, switch to patrol
        if self.current_mode == "run away" and not game_map.is_power_pellet_active():
            self.current_mode = "patrol"
            return
        
        # Check if enemy can see player
        can_see_player = self.perception.can_see_player(enemy_position, player_position, game_map)
        
        # Player spotted - start/continue chase
        if can_see_player:
            self.current_mode = "chase"
            self.chase_timer = CHASE_DURATION
            return
        
        # If sound is detected and we're not already investigating
        if sound_position is not None and self.current_mode != "investigate_sound":
            self.current_mode = "investigate_sound"
            self.sound_location = sound_position
            return
        
        # If investigating sound and reached the location
        if self.current_mode == "investigate_sound" and self.sound_location is not None:
            if enemy_position[0] == self.sound_location[0] and enemy_position[1] == self.sound_location[1]:
                # Reached the sound source, switch back to patrol
                self.current_mode = "patrol"
                self.sound_location = None
                return
        
        # Update chase timer if in chase mode
        if self.current_mode == "chase":
            self.chase_timer -= dt
            if self.chase_timer <= 0:
                # Chase timeout - go back to patrol
                self.current_mode = "patrol"
                self.chase_timer = 0
    
    def decide_move(self, enemy_position, player_position, game_map):
        """Decide the next move for the enemy based on the current mode."""
        if self.current_mode == "patrol":
            return self.patrol(enemy_position, game_map)
        elif self.current_mode == "chase":
            return self.chase(enemy_position, player_position, game_map)
        elif self.current_mode == "run away":
            return self.run_away(enemy_position, player_position, game_map)
        elif self.current_mode == "investigate_sound" and self.sound_location is not None:
            return self.investigate_sound(enemy_position, game_map)
        return self.patrol(enemy_position, game_map)  # Default to patrol
    
    def investigate_sound(self, enemy_position, game_map):
        """Investigate sound mode: Move towards the sound source."""
        if self.sound_location is None:
            return self.patrol(enemy_position, game_map)
        
        # Create distance map from the sound location
        distance_map = self.create_distance_map(self.sound_location, game_map)
        
        # Find shortest path to sound location
        best_move = (0, 0)
        shortest_distance = float('inf')

        for dx, dy in self.directions:
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                if distance_map[new_x][new_y] < shortest_distance:
                    shortest_distance = distance_map[new_x][new_y]
                    best_move = (dy, dx)

        return best_move
    
    def create_distance_map(self, start_position, game_map):
        """Creates a distance map using Dijkstra's algorithm from the start position."""
        height, width = game_map.occupancy_map.shape
        distance_map = [[float('inf') for _ in range(width)] for _ in range(height)]
        distance_map[start_position[0]][start_position[1]] = 0
        
        priority_queue = []
        heapq.heappush(priority_queue, (0, start_position[0], start_position[1]))
        
        while priority_queue:
            current_distance, current_x, current_y = heapq.heappop(priority_queue)
            
            if current_distance > distance_map[current_x][current_y]:
                continue
            for dx, dy in self.directions:
                new_x, new_y = current_x + dx, current_y + dy
                if game_map.is_valid_move(new_x, new_y):
                    new_distance = current_distance + 1
                    if new_distance < distance_map[new_x][new_y]:
                        distance_map[new_x][new_y] = new_distance
                        heapq.heappush(priority_queue, (new_distance, new_x, new_y))
        return distance_map
    
    def patrol(self, enemy_position, game_map):
        """Patrol mode: Move in a straight line until hit a wall, then change direction."""
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
    
    def chase(self, enemy_position, player_position, game_map):
        """Chase mode: Move towards the player using the shortest path."""
        distance_map = self.create_distance_map(player_position, game_map)
        
        best_move = (0, 0)
        shortest_distance = float('inf')

        for dx, dy in self.directions:
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                if distance_map[new_x][new_y] < shortest_distance:
                    shortest_distance = distance_map[new_x][new_y]
                    best_move = (dy, dx)

        return best_move
    
    def run_away(self, enemy_position, player_position, game_map):
        """Run away mode: Move away from the player as far as possible."""
        player_distance_map = self.create_distance_map(player_position, game_map)
        
        # Find the best direction to maximize distance from player
        best_move = (0, 0)
        max_distance = -1
        
        # Check all four directions
        for dx, dy in self.directions:
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                distance = player_distance_map[new_x][new_y]
                if distance == float('inf'):
                    return (dy, dx)
                
                if distance > max_distance:
                    max_distance = distance
                    best_move = (dy, dx)
        
        return best_move