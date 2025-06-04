#!/usr/bin/env python3
import pygame
import sys
import time
import random

class IntroSequence:
    def __init__(self, screen, clock, sound_system):
        self.screen = screen
        self.clock = clock
        self.sound_system = sound_system
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (50, 50, 50)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Intro sequence state
        self.current_state = 0
        self.alpha = 0  # For fade effects
        self.fade_direction = 1  # 1 for fade in, -1 for fade out
        self.text_y = self.height // 2  # For text animations
        self.player_name = ""
        self.typing_cursor_visible = True
        self.cursor_timer = 0
        
        # Loading progress
        self.loading_progress = 0
        self.loading_complete = False
        self.loading_tips = [
            "Loading your crushing student debt...",
            "Generating unrealistic job requirements...",
            "Preparing your mental health for impact...",
            "Calculating your chances of success (0.01%)...",
            "Simulating rejection emails...",
            "Inflating housing costs beyond your means...",
            "Downloading corporate buzzwords...",
            "Optimizing soul-crushing algorithms...",
            "Rendering unpaid overtime expectations...",
            "Initializing imposter syndrome...",
            "Compiling reasons why you're not good enough...",
            "Buffering existential dread..."
        ]
        self.current_tip = random.choice(self.loading_tips)
        self.tip_change_timer = 0
        
        # Timing
        self.state_timer = 0
        self.last_time = time.time()
        self.delta_time = 0
        
    def update(self):
        # Calculate delta time
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
        
        # Update state timer
        self.state_timer += self.delta_time
        
        # Update cursor blink timer
        self.cursor_timer += self.delta_time
        if self.cursor_timer >= 0.5:
            self.typing_cursor_visible = not self.typing_cursor_visible
            self.cursor_timer = 0
            
        # Update tip change timer
        self.tip_change_timer += self.delta_time
        if self.tip_change_timer >= 2.0:
            self.current_tip = random.choice(self.loading_tips)
            self.tip_change_timer = 0
        
        # State machine for intro sequence
        if self.current_state == 0:
            # Splash screen fade in
            self.alpha += 255 * self.delta_time * self.fade_direction
            if self.alpha >= 255:
                self.alpha = 255
                if self.state_timer > 3.0:
                    self.fade_direction = -1
                    
            if self.alpha <= 0 and self.fade_direction == -1:
                self.current_state = 1
                self.alpha = 0
                self.fade_direction = 1
                self.state_timer = 0
                
        elif self.current_state == 1:
            # Second splash screen
            self.alpha += 255 * self.delta_time * self.fade_direction
            if self.alpha >= 255:
                self.alpha = 255
                if self.state_timer > 3.0:
                    self.fade_direction = -1
                    
            if self.alpha <= 0 and self.fade_direction == -1:
                self.current_state = 2
                self.alpha = 255
                self.fade_direction = 1
                self.state_timer = 0
                
        elif self.current_state == 2:
            # Character creation mockup
            # Just wait for input in this state
            pass
            
        elif self.current_state == 3:
            # Loading screen
            self.loading_progress += 25 * self.delta_time
            if self.loading_progress >= 100:
                self.loading_progress = 100
                self.loading_complete = True
                
            if self.loading_complete and self.state_timer > 2.0:
                return True  # Intro sequence complete
                
        return False  # Intro sequence not complete
        
    def draw(self):
        self.screen.fill(self.BLACK)
        
        if self.current_state == 0:
            # First splash screen
            text_surface = self.font_large.render("WELCOME TO 2025...", True, self.WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
            text_surface.set_alpha(self.alpha)
            self.screen.blit(text_surface, text_rect)
            
            text_surface2 = self.font_medium.render("WHERE HAVING A DEGREE MEANS YOU'RE", True, self.WHITE)
            text_rect2 = text_surface2.get_rect(center=(self.width // 2, self.height // 2))
            text_surface2.set_alpha(self.alpha)
            self.screen.blit(text_surface2, text_rect2)
            
            text_surface3 = self.font_large.render("OVERQUALIFIED FOR ENTRY-LEVEL JOBS", True, self.RED)
            text_rect3 = text_surface3.get_rect(center=(self.width // 2, self.height // 2 + 50))
            text_surface3.set_alpha(self.alpha)
            self.screen.blit(text_surface3, text_rect3)
            
        elif self.current_state == 1:
            # Second splash screen
            text_surface = self.font_large.render("THE JOB MARKET SIMULATOR", True, self.WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
            text_surface.set_alpha(self.alpha)
            self.screen.blit(text_surface, text_rect)
            
            text_surface2 = self.font_large.render("NOBODY ASKED FOR...", True, self.WHITE)
            text_rect2 = text_surface2.get_rect(center=(self.width // 2, self.height // 2))
            text_surface2.set_alpha(self.alpha)
            self.screen.blit(text_surface2, text_rect2)
            
            text_surface3 = self.font_large.render("BUT EVERYONE NEEDS", True, self.BLUE)
            text_rect3 = text_surface3.get_rect(center=(self.width // 2, self.height // 2 + 50))
            text_surface3.set_alpha(self.alpha)
            self.screen.blit(text_surface3, text_rect3)
            
        elif self.current_state == 2:
            # Character creation mockup
            text_surface = self.font_large.render("ENTER YOUR NAME", True, self.WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
            self.screen.blit(text_surface, text_rect)
            
            text_surface2 = self.font_small.render("FOR YOUR INEVITABLE REJECTION LETTERS", True, self.RED)
            text_rect2 = text_surface2.get_rect(center=(self.width // 2, self.height // 3 + 40))
            self.screen.blit(text_surface2, text_rect2)
            
            # Draw input box
            input_box = pygame.Rect(self.width // 2 - 150, self.height // 2, 300, 40)
            pygame.draw.rect(self.screen, self.GRAY, input_box)
            pygame.draw.rect(self.screen, self.WHITE, input_box, 2)
            
            # Draw entered name
            name_surface = self.font_medium.render(self.player_name, True, self.WHITE)
            name_rect = name_surface.get_rect(midleft=(input_box.x + 10, input_box.y + input_box.height // 2))
            self.screen.blit(name_surface, name_rect)
            
            # Draw blinking cursor
            if self.typing_cursor_visible:
                cursor_x = input_box.x + 10 + name_surface.get_width()
                cursor_y = input_box.y + 5
                pygame.draw.line(self.screen, self.WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)
                
            # Draw continue button
            continue_box = pygame.Rect(self.width // 2 - 100, self.height // 2 + 60, 200, 40)
            pygame.draw.rect(self.screen, self.BLUE, continue_box)
            pygame.draw.rect(self.screen, self.WHITE, continue_box, 2)
            
            continue_text = self.font_medium.render("CONTINUE", True, self.WHITE)
            continue_rect = continue_text.get_rect(center=continue_box.center)
            self.screen.blit(continue_text, continue_rect)
            
        elif self.current_state == 3:
            # Loading screen
            text_surface = self.font_large.render("LOADING JOB RUSH 2025", True, self.WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
            self.screen.blit(text_surface, text_rect)
            
            # Draw loading bar
            loading_bar_bg = pygame.Rect(self.width // 2 - 200, self.height // 2, 400, 30)
            loading_bar_fill = pygame.Rect(self.width // 2 - 200, self.height // 2, 400 * (self.loading_progress / 100), 30)
            
            pygame.draw.rect(self.screen, self.GRAY, loading_bar_bg)
            pygame.draw.rect(self.screen, self.BLUE, loading_bar_fill)
            pygame.draw.rect(self.screen, self.WHITE, loading_bar_bg, 2)
            
            # Draw loading percentage
            percent_text = self.font_small.render(f"{int(self.loading_progress)}%", True, self.WHITE)
            percent_rect = percent_text.get_rect(center=loading_bar_bg.center)
            self.screen.blit(percent_text, percent_rect)
            
            # Draw loading tip
            tip_text = self.font_medium.render(self.current_tip, True, self.RED)
            tip_rect = tip_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
            self.screen.blit(tip_text, tip_rect)
            
            if self.loading_complete:
                complete_text = self.font_medium.render("PRESS ANY KEY TO START", True, self.WHITE)
                complete_rect = complete_text.get_rect(center=(self.width // 2, self.height // 2 + 150))
                
                # Make it blink
                if self.typing_cursor_visible:
                    self.screen.blit(complete_text, complete_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if self.current_state == 2:  # Only handle name input in state 2
                    if event.key == pygame.K_RETURN:
                        if self.player_name:  # Only proceed if name is not empty
                            self.sound_system.play_sound("button_click")
                            return self.player_name
                    elif event.key == pygame.K_BACKSPACE:
                        self.sound_system.play_sound("button_click")
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) < 20:
                        self.sound_system.play_sound("button_click")
                        self.player_name += event.unicode
        return None
        
    def run(self):
        """Run the intro sequence until completion"""
        intro_complete = False
        
        while not intro_complete:
            intro_complete = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            
        return self.player_name  # Return the entered player name

if __name__ == "__main__":
    # Test the intro sequence
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Job Rush 2025 - Intro Test")
    clock = pygame.time.Clock()
    
    intro = IntroSequence(screen, clock)
    player_name = intro.run()
    
    print(f"Player name: {player_name}")
    pygame.quit()
    sys.exit()
