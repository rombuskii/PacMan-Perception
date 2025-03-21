import pygame
from config import DIRECTIONS, GAME_TITLE, FPS, GAME_SPEED
from map import Map
from entities import EntityManager
from render import Renderer

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        
        # Create game components
        self.game_map = Map()
        self.entity_manager = EntityManager(self.game_map)
        self.renderer = Renderer()
        
        # Game state
        self.running = True
        
        # Initialize clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Time tracking for fixed update step
        self.last_update_time = 0
        self.update_interval = 1000 / GAME_SPEED  # Milliseconds between game updates

    # Process pygame events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key in DIRECTIONS:
                # Get the new direction
                new_direction = DIRECTIONS[event.key]
                
                # Check if the move would be valid in this direction
                player = self.entity_manager.player
                new_x = player.position[0] + new_direction[1]
                new_y = player.position[1] + new_direction[0]
                
                # Only change direction if the move is valid
                if self.game_map.is_valid_move(new_x, new_y):
                    player.current_direction = new_direction
    
    # Update game state
    def update(self):
        # Continue player movement in current direction
        self.entity_manager.continue_player_movement()
        
        # Move enemies
        self.entity_manager.move_enemies()
        
        # Check for collisions
        if self.entity_manager.check_collision():
            print("Game Over! You were caught.")
            self.running = False
        
        # Check for win condition
        if self.game_map.check_win():
            print("Congratulations! You collected all points.")
            self.running = False
    
    # Render the game
    def render(self):
        self.renderer.render(self.game_map, self.entity_manager)
    
    # Main game loop
    def run(self):
        while self.running:
            self.handle_events()
            
            # Check if it's time for a game update
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= self.update_interval:
                self.update()
                self.last_update_time = current_time
            
            self.render()
            
            # Maintain the frame rate for smooth rendering
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
