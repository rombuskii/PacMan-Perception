import numpy as np
import random
from config import ROWS, COLS

class Map:
    def __init__(self, wall_probability=0.1):
        self.occupancy_map = np.zeros((ROWS, COLS))
        self.generate_map(wall_probability)
    
    # Generate a random map with walls and collectible points
    def generate_map(self, wall_probability):
        for i in range(ROWS):
            for j in range(COLS):
                if random.random() < wall_probability:
                    self.occupancy_map[i, j] = -1  # Wall
                else:
                    self.occupancy_map[i, j] = 1  # Collectible point
    
    # Set a position as empty (no collectible)
    def set_position_empty(self, x, y):
        if 0 <= x < ROWS and 0 <= y < COLS:
            self.occupancy_map[x, y] = 0
    
    # Check if a position is valid for movement
    def is_valid_move(self, x, y):
        return 0 <= x < ROWS and 0 <= y < COLS and self.occupancy_map[x, y] != -1
    
    # Collect a point at the given position
    def collect_point(self, x, y):
        if self.occupancy_map[x, y] == 1:
            self.occupancy_map[x, y] = 0
            return True
        return False
    
    # Check if all collectible points have been collected
    def check_win(self):
        return np.sum(self.occupancy_map == 1) == 0 