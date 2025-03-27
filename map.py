import numpy as np
from config import ROWS, COLS

class Map:
    def __init__(self, wall_probability=0.1):
        self.occupancy_map = np.zeros((ROWS, COLS))
        self.generate_pacman_map()
    
    # Generate a Pac-Man style map with walls and collectible points based on the specific layout
    def generate_pacman_map(self):
        # Define the layout with a larger scale
        pacman_layout = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W..........................S..W",
            "W.WWWWW.WWWWWWW.WWWWWWW.WWWWW.W",
            "W.W   W.W     W.W     W.W   W.W",
            "W.W   W.W     W.W     W.W   W.W",
            "W.WWWWW.WWWWWWW.WWWWWWW.WWWWW.W",
            "W.............................W",
            "W.WWWWW.WW.WWWWWWWWW.WW.WWWWW.W",
            "W.WWWWW.WW.WWWWWWWWW.WW.WWWWW.W",
            "W.......WW.....W.....WW.......W",
            "WWWWWWW.WWWWW  W  WWWWW.WWWWWWW",
            "      W.WWWWW  W  WWWWW.W      ",
            "      W.WW           WW.W      ",
            "      W.WW           WW.W      ",
            "      W.WW           WW.W      ",
            "      W.               .W      ",
            "      W.WW           WW.W      ",
            "      W.WW           WW.W      ",
            "      W.WW           WW.W      ",
            "      W.WW           WW.W      ",
            "      W.WW  WWWWWWW  WW.W      ",
            "WWWWWWW.WW  WWWWWWW  WW.WWWWWWW",
            "W.............................W",
            "W.WWWWW.WWWWW.W.W.WWWWW.WWWWW.W",
            "W.WWWWW.WWWWW.W.W.WWWWW.WWWWW.W",
            "W...WW..............WW........W",
            "WWW.WW.WW.WWWWWWWWW.WW.WW.WWWWW",
            "WWW.WW.WW.WWWWWWWWW.WW.WW.WWWWW",
            "W.............................W",
            "W.WWWWWWWWWWW.W.W.WWWWWWWWWWW.W",
            "W.WWWWWWWWWWW.W.W.WWWWWWWWWWW.W",
            "W.............................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        ]
        
        # Reset the map to proper size
        actual_rows = len(pacman_layout)
        actual_cols = len(pacman_layout[0])
        
        # Create a new occupancy map with the right dimensions
        self.occupancy_map = np.zeros((actual_rows, actual_cols))
        
        # Fill the map based on the layout
        for i, row in enumerate(pacman_layout):
            for j, cell in enumerate(row):
                if cell == 'W':  # Wall
                    self.occupancy_map[i, j] = -1
                elif cell == '.':  # Regular pellet
                    self.occupancy_map[i, j] = 1
                elif cell == 'S':  # Sound pellet
                    self.occupancy_map[i, j] = 3
                elif cell == ' ':  # Empty space
                    self.occupancy_map[i, j] = 0
    
    # Set a position as empty (no collectible)
    def set_position_empty(self, x, y):
        if 0 <= x < self.occupancy_map.shape[0] and 0 <= y < self.occupancy_map.shape[1]:
            self.occupancy_map[x, y] = 0
    
    # Check if a position is valid for movement
    def is_valid_move(self, x, y):
        return (0 <= x < self.occupancy_map.shape[0] and 
                0 <= y < self.occupancy_map.shape[1] and 
                self.occupancy_map[x, y] != -1)
    
    # Collect a point at the given position
    def collect_point(self, x, y):
        if self.occupancy_map[x, y] in [1, 2, 3]:  # Regular, power, or sound pellet
            is_power_pellet = (self.occupancy_map[x, y] == 2)
            is_sound_pellet = (self.occupancy_map[x, y] == 3)
            self.occupancy_map[x, y] = 0
            return True, is_power_pellet, is_sound_pellet
        return False, False, False
    
    # Check if all collectible points have been collected
    def check_win(self):
        return np.sum(self.occupancy_map == 1) == 0 and np.sum(self.occupancy_map == 2) == 0

    def generate_map(self, wall_probability):
        # Kept for backward compatibility
        self.generate_pacman_map() 