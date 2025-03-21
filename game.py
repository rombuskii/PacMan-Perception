import pygame
from config import DIRECTIONS, GAME_TITLE, FRAME_DELAY
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

    # Process pygame events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key in DIRECTIONS:
                self.entity_manager.move_player(DIRECTIONS[event.key])
    
    # Update game state
    def update(self):
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
            self.update()
            self.render()
            pygame.time.delay(FRAME_DELAY)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
