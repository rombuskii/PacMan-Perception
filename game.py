import pygame
from config import DIRECTIONS, GAME_TITLE, FPS, GAME_SPEED, DISTANCE_MAP_VISIBLE
from map import Map
from entities import EntityManager
from render import Renderer

class Game:
    def __init__(self):
        """Initialize the game components and state."""
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        
        # Create game components
        self.game_map = Map()
        self.entity_manager = EntityManager(self.game_map)
        self.renderer = Renderer()
        
        # Add enemies to the game
        self._setup_enemies()
        
        # Connect renderer to entity manager for sound effects
        self.entity_manager.set_renderer(self.renderer)
        
        # Game state
        self.running = True
        self.show_distance_map = DISTANCE_MAP_VISIBLE
        self.current_distance_map = None
        
        # Time tracking
        self.clock = pygame.time.Clock()
        self.last_update_time = 0
        self.update_interval = 1000 / GAME_SPEED  # Milliseconds between updates
    
    def _setup_enemies(self):
        """Set up enemy entities in the game."""
        self.entity_manager.add_enemy(x=5, y=11)
        # Add more enemies as needed
        # self.entity_manager.add_enemy(x=10, y=11)

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
    
    def _handle_keydown(self, event):
        """Process keyboard inputs."""
        # Handle movement keys
        if event.key in DIRECTIONS:
            self._process_movement_input(DIRECTIONS[event.key])
        # Toggle distance map visualization with 'D' key
        elif event.key == pygame.K_d:
            self._toggle_distance_map()
    
    def _process_movement_input(self, new_direction):
        """Process player movement input."""
        player = self.entity_manager.player
        player.intended_direction = new_direction
        
        # Only set current_direction if the move is valid
        new_x = player.position[0] + new_direction[1]
        new_y = player.position[1] + new_direction[0]
        if self.game_map.is_valid_move(new_x, new_y):
            player.current_direction = new_direction
    
    def _toggle_distance_map(self):
        """Toggle the distance map visualization on/off."""
        self.show_distance_map = not self.show_distance_map
        print(f"Distance map visualization: {'ON' if self.show_distance_map else 'OFF'}")
        
        # Immediately calculate the distance map when turning visualization on
        if self.show_distance_map and len(self.entity_manager.enemies) > 0:
            self._update_distance_map()
            print("Distance map calculated")
    
    def _update_distance_map(self):
        """Update the distance map for visualization."""
        if len(self.entity_manager.enemies) > 0:
            enemy = self.entity_manager.enemies[0]
            player_pos = self.entity_manager.player.position
            self.current_distance_map = enemy.ai.create_distance_map(player_pos, self.game_map)
    
    def update(self):
        """Update game state for one time step."""
        # Update map state (power pellet duration, etc.)
        self.game_map.update()
        
        # Continue player movement in current direction
        self.entity_manager.continue_player_movement()
        
        # Update the distance map if visualization is enabled
        if self.show_distance_map:
            self._update_distance_map()
        
        # Move enemies
        self.entity_manager.move_enemies()
        
        # Check game end conditions
        self._check_game_end_conditions()
    
    def _check_game_end_conditions(self):
        """Check if the game should end."""
        # Check for collisions
        if self.entity_manager.check_collision():
            print("Game Over! You were caught.")
            self.running = False
        
        # Check for win condition
        if self.game_map.check_win():
            print("Congratulations! You collected all points.")
            self.running = False
    
    def render(self):
        """Render the current game state."""
        self.renderer.render(
            self.game_map, 
            self.entity_manager, 
            show_distance_map=self.show_distance_map, 
            distance_map=self.current_distance_map
        )
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            
            # Update game at fixed time intervals
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= self.update_interval:
                self.update()
                self.last_update_time = current_time

            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
