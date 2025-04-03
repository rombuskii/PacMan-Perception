import numpy as np
from config import *

class Map:
    """
    Map class handles the game world representation including walls,
    pellets, and collision detection.
    """
    
    # Cell type constants
    WALL = -1
    EMPTY = 0
    REGULAR_PELLET = 1
    POWER_PELLET = 2
    SOUND_PELLET = 3
    
    def __init__(self, wall_probability=0.1):
        """Initialize the game map with a Pac-Man style layout."""
        self.occupancy_map = np.zeros((ROWS, COLS))
        self.power_pellet_active = False
        self.power_pellet_duration = 0
        self.generate_pacman_map()
    
    def generate_pacman_map(self):
        """Generate a Pac-Man style map with walls and collectible points."""
        # Define the layout with a larger scale
        pacman_layout = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W..........................S..W",
            "W.WWWWW.WWWWWWWPWWWWWWW.WWWWW.W",
            "W.W   W.W     W.W     W.W   W.W",
            "W.W   W.W     W.W     W.W   W.W",
            "W.WWWWW.WWWWWWW.WWWWWWW.WWWWW.W",
            "W.............................W",
            "W.WWWWW.WW.WWWWWWWWW.WW.WWWWW.W",
            "W.WWWWW.WW.WWWWWWWWW.WW.WWWWW.W",
            "W.......WW.....W.....WW.......W",
            "WWWWWWW.WWWWW.WW.WWWWWW.WWWWWWW",
            "      W.WWWWW.WW.WWWWWW.W      ",
            "      W.................W      ",
            "      W.WWWWWWWWWWWWWWW.W      ",
            "      W.................W      ",
            "      W.WWWWWWWWWWWWWWW.W      ",
            "      W.................W      ",
            "      W.WWWWWWWWWWWWWWW.W      ",
            "      W.................W      ",
            "      W.WW.WWWWWWWW.WWW.W      ",
            "      W.WW.WWWWWWWW.WWW.W      ",
            "WWWWWWW.WW.WWWWWWWW.WWW.WWWWWWW",
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
        
        # Create a new occupancy map with the right dimensions
        actual_rows = len(pacman_layout)
        actual_cols = len(pacman_layout[0])
        self.occupancy_map = np.zeros((actual_rows, actual_cols))
        
        # Fill the map based on the layout
        self._populate_map_from_layout(pacman_layout)
    
    def _populate_map_from_layout(self, layout):
        """Convert the text layout to the numerical occupancy map."""
        for i, row in enumerate(layout):
            for j, cell in enumerate(row):
                if cell == 'W':  # Wall
                    self.occupancy_map[i, j] = self.WALL
                elif cell == '.':  # Regular pellet
                    self.occupancy_map[i, j] = self.REGULAR_PELLET
                elif cell == 'P':  # Power pellet
                    self.occupancy_map[i, j] = self.POWER_PELLET
                elif cell == 'S':  # Sound pellet
                    self.occupancy_map[i, j] = self.SOUND_PELLET
                elif cell == ' ':  # Empty space
                    self.occupancy_map[i, j] = self.EMPTY
    
    def set_position_empty(self, x, y):
        """Set a position as empty (no collectible)."""
        if self._is_valid_position(x, y):
            self.occupancy_map[x, y] = self.EMPTY
    
    def is_valid_move(self, x, y):
        """Check if a position is valid for movement (not a wall and within bounds)."""
        return (self._is_valid_position(x, y) and self.occupancy_map[x, y] != self.WALL)
    
    def _is_valid_position(self, x, y):
        """Check if a position is within the map bounds."""
        return (0 <= x < self.occupancy_map.shape[0] and 
                0 <= y < self.occupancy_map.shape[1])
    
    def collect_point(self, x, y):
        """
        Collect a point at the given position.
        Returns (collected, is_power_pellet, is_sound_pellet).
        """
        cell_value = self.occupancy_map[x, y]
        
        if cell_value in [self.REGULAR_PELLET, self.POWER_PELLET, self.SOUND_PELLET]:
            is_power_pellet = (cell_value == self.POWER_PELLET)
            is_sound_pellet = (cell_value == self.SOUND_PELLET)
            
            # Activate power pellet effect if collected
            if is_power_pellet:
                self._activate_power_pellet()
            
            # Clear the cell
            self.occupancy_map[x, y] = self.EMPTY
            return True, is_power_pellet, is_sound_pellet
            
        return False, False, False
    
    def _activate_power_pellet(self):
        """Activate the power pellet effect for a duration."""
        self.power_pellet_active = True
        self.power_pellet_duration = POWER_PELLET_DURATION  # Use value from config.py
    
    def update(self):
        """Update the map state (e.g., power pellet duration)."""
        if self.power_pellet_active:
            self.power_pellet_duration -= 1
            if self.power_pellet_duration <= 0:
                self.power_pellet_active = False
    
    def check_win(self):
        """Check if all collectible points have been collected."""
        return (np.sum(self.occupancy_map == self.REGULAR_PELLET) == 0 and 
                np.sum(self.occupancy_map == self.POWER_PELLET) == 0)
    
    def is_power_pellet_active(self):
        """Check if a power pellet effect is currently active."""
        return self.power_pellet_active
    
    def generate_map(self, wall_probability):
        """Legacy method kept for backward compatibility."""
        self.generate_pacman_map() 