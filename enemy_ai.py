import heapq

class EnemyPerception:
    def __init__(self):
        self.perception_range = 10  # Default perception range
    
    def calculate_distance(self, start_position, target_position):
        """Calculate the Manhattan distance between two positions."""
        return abs(start_position[0] - target_position[0]) + abs(start_position[1] - target_position[1])
    
    def can_see_player(self, enemy_position, player_position, game_map):
        """Check if the enemy can see the player within the perception range."""
        distance = self.calculate_distance(enemy_position, player_position)
        return distance <= self.perception_range
        
class EnemyAI:
    def __init__(self):
        self.perception = EnemyPerception()
        self.current_mode = "patrol"  # patrol, chase, run away
        self.patrol_direction = [0, 1]  # Initialize with a default direction
        self.is_horizontal = True  # Track if moving horizontally or vertically
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    def update_mode(self, enemy_position, player_position, game_map):
        """Update the AI mode based on the game state."""
        if self.perception.can_see_player(enemy_position, player_position, game_map):
            if game_map.is_power_pellet_active():
                self.current_mode = "run away"
            else:
                self.current_mode = "chase"
        else:
            self.current_mode = "patrol"
    
    def decide_move(self, enemy_position, player_position, game_map):
        """Decide the next move for the enemy based on the current mode."""
        if self.current_mode == "patrol":
            return self.patrol(enemy_position, game_map)
        elif self.current_mode == "chase":
            return self.chase(enemy_position, player_position, game_map)
        elif self.current_mode == "run away":
            return self.run_away(enemy_position, player_position, game_map)
    
    def create_distance_map(self, start_position, game_map):
        """Creates a distance map using Dijkstra's algorithm from the start position."""
        # Get the dimensions of the map
        height, width = game_map.occupancy_map.shape
        
        # Initialize distance map with infinity for all cells
        distance_map = [[float('inf') for _ in range(width)] for _ in range(height)]
        
        # Set distance for starting position
        distance_map[start_position[0]][start_position[1]] = 0
        
        # Initialize the priority queue for Dijkstra's algorithm
        priority_queue = []
        heapq.heappush(priority_queue, (0, start_position[0], start_position[1]))
        
        # Process queue until empty
        while priority_queue:
            # Get cell with smallest distance
            current_distance, current_x, current_y = heapq.heappop(priority_queue)
            
            # If we've already found a better path to this cell, skip it
            if current_distance > distance_map[current_x][current_y]:
                continue
            
            # Check all neighbors
            for dx, dy in self.directions:
                new_x, new_y = current_x + dx, current_y + dy
                
                # Check if the move is valid (within bounds and not a wall)
                if game_map.is_valid_move(new_x, new_y):
                    # Calculate new distance (1 unit per move)
                    new_distance = current_distance + 1
                    
                    # If we found a better path, update the distance
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
                    best_move = (dx, dy)

        return best_move
    
    def run_away(self, enemy_position, player_position, game_map):
        """Run away mode: Move away from the player using the longest path."""
        distance_map = self.create_distance_map(player_position, game_map)
        best_move = (0, 0)
        longest_distance = -1

        for dx, dy in self.directions:
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                if distance_map[new_x][new_y] > longest_distance:
                    longest_distance = distance_map[new_x][new_y]
                    best_move = (dx, dy)

        return best_move

