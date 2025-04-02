import pygame
from config import DIRECTIONS, GAME_TITLE, FPS, GAME_SPEED, DISTANCE_MAP_VISIBLE
from map import Map
from entities import EntityManager
from render import Renderer

class GameOverScreen:
    def __init__(self, screen, width, height, score=0):
        self.screen = screen
        self.width = width
        self.height = height
        self.score = score
        
        # Load or create fonts
        try:
            self.title_font = pygame.font.Font("fonts/arcade.ttf", 80)  # Arcade-style font if available
        except:
            self.title_font = pygame.font.Font(None, 80)
            
        try:
            self.menu_font = pygame.font.Font("fonts/arcade.ttf", 36)
        except:
            self.menu_font = pygame.font.Font(None, 40)
            
        # Animation properties
        self.flash_speed = 500  # Flash interval in milliseconds
        self.last_flash_time = 0
        self.show_text = True
        
        # Colors
        self.colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "pink": (255, 192, 203),
            "orange": (255, 165, 0),
            "cyan": (0, 255, 255)
        }
        
        # Initialize ghosts
        self.ghosts = []
        ghost_colors = [self.colors["red"], self.colors["pink"], 
                        self.colors["cyan"], self.colors["orange"]]
        
        for color in ghost_colors:
            self.ghosts.append({
                "x": pygame.time.get_ticks() % width,  # Distribute ghosts across screen
                "y": 100 + (ghost_colors.index(color) * 50),  # Stack ghosts vertically with spacing
                "speed": 2 + (ghost_colors.index(color) * 0.5),  # Different speeds
                "color": color,
                "direction": 1 if ghost_colors.index(color) % 2 == 0 else -1  # Alternate directions
            })
            
        # Pac-Man death animation frames
        self.pacman_death_frames = 12
        self.current_frame = 0
        self.frame_delay = 8
        self.frame_counter = 0
        
        # Message to display
        self.message = "Game Over!"
        
        # Try to play a death sound
        try:
            self.death_sound = pygame.mixer.Sound("sounds/death.wav")
            self.death_sound.play()
        except:
            pass  # Sound is optional

    def set_message(self, message):
        """Set the message to display on the game over screen."""
        self.message = message

    def draw_ghost(self, x, y, color):
        """Draw a classic Pac-Man ghost"""
        # Body
        ghost_width = 40
        ghost_height = 40
        
        # Main body (semi-oval)
        pygame.draw.ellipse(self.screen, color, 
                           (x - ghost_width//2, y - ghost_height//2, 
                            ghost_width, ghost_height))
        
        # Bottom part with waves (three rectangles)
        wave_height = 10
        for i in range(3):
            wave_width = ghost_width // 3
            pygame.draw.rect(self.screen, color, 
                            (x - ghost_width//2 + i*wave_width, 
                             y + ghost_height//2 - wave_height,
                             wave_width, wave_height))
            
        # White of eyes
        eye_radius = 7
        pygame.draw.circle(self.screen, self.colors["white"], 
                          (x - 10, y - 7), eye_radius)
        pygame.draw.circle(self.screen, self.colors["white"], 
                          (x + 10, y - 7), eye_radius)
        
        # Blue pupils (looking in movement direction)
        pupil_radius = 3
        direction = 1 if color == self.colors["red"] else -1  # Red ghost goes right
        
        pygame.draw.circle(self.screen, self.colors["blue"], 
                          (x - 10 + 3*direction, y - 7), pupil_radius)
        pygame.draw.circle(self.screen, self.colors["blue"], 
                          (x + 10 + 3*direction, y - 7), pupil_radius)

    def draw_pacman_death(self, x, y):
        """Draw Pac-Man's death animation"""
        # Animation is a circle opening from bottom to top
        if self.current_frame <= self.pacman_death_frames:
            angle = 180 - (180 * self.current_frame / self.pacman_death_frames)
            start_angle = angle
            end_angle = 360 - angle
            
            pygame.draw.arc(self.screen, self.colors["yellow"], 
                           (x - 30, y - 30, 60, 60),
                           pygame.math.Vector2(0, -1).angle_to(pygame.math.Vector2(1, 0)) * (start_angle/360),
                           pygame.math.Vector2(0, -1).angle_to(pygame.math.Vector2(1, 0)) * (end_angle/360), 30)

    def display_score(self):
        """Display the final score"""
        score_text = self.menu_font.render(f"FINAL SCORE: {self.score}", True, self.colors["white"])
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(score_text, score_rect)

    def display(self):
        """Display the enhanced Game Over screen with animations"""
        # For Pac-Man death animation initial positioning
        pacman_x = self.width // 2
        pacman_y = self.height // 3 + 100
        
        # Initialize tick clock for maintaining FPS
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(self.colors["black"])
            
            # Maze background effect (faint grid lines)
            for x in range(0, self.width, 30):
                pygame.draw.line(self.screen, (20, 20, 70), (x, 0), (x, self.height), 1)
            for y in range(0, self.height, 30):
                pygame.draw.line(self.screen, (20, 20, 70), (0, y), (self.width, y), 1)

            # Flashing "GAME OVER" text effect
            current_time = pygame.time.get_ticks()
            if current_time - self.last_flash_time > self.flash_speed:
                self.show_text = not self.show_text
                self.last_flash_time = current_time

            if self.show_text:
                # Draw with shadow for better visibility
                game_over_shadow = self.title_font.render(self.message, True, (100, 0, 0))
                game_over_text = self.title_font.render(self.message, True, self.colors["red"])
                
                shadow_pos = (self.width // 2 - game_over_shadow.get_width() // 2 + 3, 
                              self.height // 4 + 3)
                text_pos = (self.width // 2 - game_over_text.get_width() // 2, 
                            self.height // 4)
                
                self.screen.blit(game_over_shadow, shadow_pos)
                self.screen.blit(game_over_text, text_pos)

            # Pac-Man death animation
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                if self.current_frame <= self.pacman_death_frames:
                    self.current_frame += 1
                    
            self.draw_pacman_death(pacman_x, pacman_y)
            
            # Moving ghosts in the background
            for ghost in self.ghosts:
                ghost["x"] += ghost["speed"] * ghost["direction"]
                
                # Bounce ghosts off the edges
                if ghost["x"] < -30 or ghost["x"] > self.width + 30:
                    ghost["direction"] *= -1
                    
                self.draw_ghost(ghost["x"], ghost["y"], ghost["color"])

            # Display score
            self.display_score()
            
            # Option buttons with highlighting on hover
            mouse_pos = pygame.mouse.get_pos()
            
            # Restart button
            restart_text = self.menu_font.render("RESTART", True, self.colors["yellow"])
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height * 0.7))
            
            # Highlight on hover
            if restart_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (60, 60, 60), 
                               restart_rect.inflate(20, 10), border_radius=5)
            
            self.screen.blit(restart_text, restart_rect)
            
            # Quit button
            quit_text = self.menu_font.render("QUIT", True, self.colors["yellow"])
            quit_rect = quit_text.get_rect(center=(self.width // 2, self.height * 0.8))
            
            # Highlight on hover
            if quit_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (60, 60, 60), 
                               quit_rect.inflate(20, 10), border_radius=5)
                
            self.screen.blit(quit_text, quit_rect)

            pygame.display.flip()  # Update display

            # Handle input events
            action = self.handle_input(restart_rect, quit_rect)
            if action:
                return action

            # Control frame rate
            clock.tick(60)

    def handle_input(self, restart_rect, quit_rect):
        """Handle input during the Game Over screen with mouse support."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                elif quit_rect.collidepoint(event.pos):
                    return "quit"
        return None


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
        
        # Score tracking
        self.score = 0
    
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
            
    def show_game_over_screen(self, message):
        """Display an enhanced Game Over screen with the given message."""
        # Update the final score - You might need to adjust how score is tracked in your game
        self.update_score()
        self.score = self.game_map.total_score
        
        # Create and display the game over screen
        screen_width = self.renderer.screen.get_width()
        screen_height = self.renderer.screen.get_height()
        
        game_over = GameOverScreen(self.renderer.screen, screen_width, screen_height, self.score)
        game_over.set_message(message)
        
        action = game_over.display()
        
        if action == "restart":
            self.reset_game()
        elif action == "quit":
            self.running = False
    
    def update_score(self):
        regular_pellet_points = 10
        power_pellet_points = 50
        sound_pellet_points = 30

    # Count each type of pellet from the occupancy map
        if not hasattr(self.game_map, 'regular_pellets_collected'):
        # Initialize counters
            self.game_map.regular_pellets_collected = 0
            self.game_map.power_pellets_collected = 0
            self.game_map.sound_pellets_collected = 0
            self.game_map.total_score = 0

        # Monkey patch the collect_point method to track collections
            original_collect_point = self.game_map.collect_point

            def collect_point_with_score(x, y):
                collected, is_power, is_sound = original_collect_point(x, y)

                if collected:
                    if is_power:
                        self.game_map.power_pellets_collected += 1
                        self.game_map.total_score += power_pellet_points
                    elif is_sound:
                        self.game_map.sound_pellets_collected += 1
                        self.game_map.total_score += sound_pellet_points
                    else:
                        self.game_map.regular_pellets_collected += 1
                        self.game_map.total_score += regular_pellet_points

                return collected, is_power, is_sound

            self.game_map.collect_point = collect_point_with_score

        # Ensure score updates
        self.score = self.game_map.total_score
    
    def reset_game(self):
        """Reset the game to start a new round."""
        # Reset map
        self.game_map = Map()
        
        # Reset entities
        self.entity_manager = EntityManager(self.game_map)
        self.entity_manager.set_renderer(self.renderer)
        self._setup_enemies()
        
        # Reset game state
        self.show_distance_map = DISTANCE_MAP_VISIBLE
        self.current_distance_map = None
        self.last_update_time = pygame.time.get_ticks()
        self.score = 0
        
        # Continue running
        self.running = True
    
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
        if self.entity_manager.check_collision():
            self.show_game_over_screen("GAME OVER")
    
        if self.game_map.check_win():
            self.show_game_over_screen("YOU WIN!")
    
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