import heapq


class EnemyPerception:
    def __init__(self):
        self.perception_range = 10  # Default perception range
    
    def calculate_distance(self, start_position, target_position):
        """
        Calculate the Manhattan distance between two positions.
        """
        return abs(start_position[0] - target_position[0]) + abs(start_position[1] - target_position[1])
    
    def can_see_player(self, enemy_position, player_position, game_map):
        """
        Check if the enemy can see the player within the perception range.
        """
        distance = self.calculate_distance(enemy_position, player_position)
        return distance <= self.perception_range
        

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
    def decide_move(self, enemy_position, player_position, game_map):
         """
        Decide the next move for the enemy based on the current mode.
        """
         if self.current_mode == "patrol":
            return self.patrol(enemy_position, game_map)
         elif self.current_mode == "chase":
            return self.chase(enemy_position, player_position, game_map)
         elif self.current_mode == "run away":
            return self.run_away(enemy_position, player_position, game_map)
        
    def update_mode(self, enemy_position, player_position, game_map):
        """
        Update the AI mode based on the game state.
        """
        #if self.perception.can_see_player(enemy_position, player_position, game_map):
            #if game_map.is_power_pellet_active():
        pass


def create_distance_map(self, start_position, game_map):
        """
        Creates a distance map using Dijkstra's algorithm from the start position.
        """
        rows, cols = len(game_map), len(game_map[0])
        distance_map = [[float('inf')] * cols for _ in range(rows)]
        distance_map[start_position[0]][start_position[1]] = 0

        priority_queue = [(0, start_position)]  # (distance, (x, y))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        while priority_queue:
            current_distance, (current_x, current_y) = heapq.heappop(priority_queue)

            if current_distance > distance_map[current_x][current_y]:
                continue

            for dx, dy in directions:
                neighbor_x, neighbor_y = current_x + dx, current_y + dy

                if game_map.is_valid_move(neighbor_x, neighbor_y):
                    new_distance = current_distance + 1

                    if new_distance < distance_map[neighbor_x][neighbor_y]:
                        distance_map[neighbor_x][neighbor_y] = new_distance
                        heapq.heappush(priority_queue, (new_distance, (neighbor_x, neighbor_y)))

        return distance_map
    
    
def patrol(self, enemy_position, game_map):
        """
        Patrol mode: Move randomly or follow a predefined path.
        """
        #directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        directions = [(0, 1), (0, -1)]
        valid_moves = []
        for dx, dy in directions:
            #0 <= x < self.occupancy_map.shape[0] and 0 <= y < self.occupancy_map.shape[1]
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                valid_moves.append((dx, dy))
        if valid_moves:
            return valid_moves[0]  # Move randomly in a valid direction
        return (0, 0)  # Stay in place if no valid moves
    
def chase(self, enemy_position, player_position, game_map):
        """
        Chase mode: Move towards the player using the shortest path.
        """
        distance_map = self.create_distance_map(player_position, game_map)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        best_move = (0, 0)
        shortest_distance = float('inf')

        for dx, dy in directions:
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                if distance_map[new_x][new_y] < shortest_distance:
                    shortest_distance = distance_map[new_x][new_y]
                    best_move = (dx, dy)

        return best_move
    
def run_away(self, enemy_position, player_position, game_map):
        """
        Run away mode: Move away from the player using the longest path.
        """
        distance_map = self.create_distance_map(player_position, game_map)
        ## Left, Right, Up, Down respectively.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        best_move = (0, 0)
        longest_distance = -1

        for dx, dy in directions:
            new_x, new_y = enemy_position[0] + dx, enemy_position[1] + dy
            if game_map.is_valid_move(new_x, new_y):
                if distance_map[new_x][new_y] > longest_distance:
                    longest_distance = distance_map[new_x][new_y]
                    best_move = (dx, dy)

        return best_move

