import pygame
import math
import random

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
        
        # Load ghost images or use placeholder
        self.ghosts = []
        ghost_colors = [self.colors["red"], self.colors["pink"], 
                        self.colors["cyan"], self.colors["orange"]]
        
        for color in ghost_colors:
            self.ghosts.append({
                "x": random.randint(-50, self.width),
                "y": random.randint(100, self.height - 100),
                "speed": random.uniform(2, 5),
                "color": color,
                "direction": random.choice([-1, 1])
            })
            
        # Pac-Man death animation frames
        self.pacman_death_frames = 12
        self.current_frame = 0
        self.frame_delay = 8
        self.frame_counter = 0
        
        # Sound effects
        try:
            self.death_sound = pygame.mixer.Sound("sounds/death.wav")
            self.death_sound.play()
        except:
            pass  # Sound is optional

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
                           math.radians(start_angle), 
                           math.radians(end_angle), 30)

    def display_score(self):
        """Display the final score"""
        score_text = self.menu_font.render(f"FINAL SCORE: {self.score}", True, self.colors["white"])
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)

    def display_high_scores(self):
        """Display high scores section"""
        # This could be expanded to load and save actual high scores
        hs_text = self.menu_font.render("HIGH SCORES", True, self.colors["yellow"])
        hs_rect = hs_text.get_rect(center=(self.width // 2, self.height // 2 + 100))
        self.screen.blit(hs_text, hs_rect)

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
                game_over_shadow = self.title_font.render("GAME OVER", True, (100, 0, 0))
                game_over_text = self.title_font.render("GAME OVER", True, self.colors["red"])
                
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