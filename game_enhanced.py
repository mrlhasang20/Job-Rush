#!/usr/bin/env python3
import pygame
import sys
import random
import time
from enum import Enum
import textwrap

# Import our components
from player_enhanced import Player
from obstacles_enhanced import Obstacle, PowerUp
from visual_elements import ParallaxBackground, ParticleSystem, SpriteManager
from popup_system import PopupSystem
from game_over import GameOverScreen
from intro_sequence import IntroSequence
from corporate_jargon import CorporateJargonGenerator
from sound_system import SoundSystem

class GameState(Enum):
    INTRO = 0
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    PAUSED = 4

class Sector(Enum):
    TECH = 4
    ACADEMIA = 1
    CREATIVE = 2
    RETAIL = 3
    SILICON_VALLEY = 0

class Game:
    def __init__(self, screen, clock, audio_available=True):
        self.screen = screen
        self.clock = clock
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize sound system FIRST
        self.sound_system = SoundSystem(audio_available)
        
        # Calculate lane positions BEFORE reset_game
        self.lane_height = self.height // 3
        self.lane_positions = [
            self.lane_height // 2, 
            self.lane_height + self.lane_height // 2, 
            2 * self.lane_height + self.lane_height // 2
        ]
        
        # Initialize sector and transition score BEFORE creating background
        self.sector = "SILICON_VALLEY"
        self.sector_transition_score = 500
        
        # Initialize components
        self.sprite_manager = SpriteManager()
        self.particle_system = ParticleSystem()
        self.background = ParallaxBackground(self.width, self.height, self.sector)
        self.popup_system = PopupSystem(self.width, self.height)
        self.popup_system.set_sound_system(self.sound_system)
        self.jargon_generator = CorporateJargonGenerator()
        
        # Game state
        self.state = GameState.INTRO
        self.player_name = ""
        
        # Initialize game objects
        self.reset_game()
        
        # Timing
        self.last_time = time.time()
        self.delta_time = 0
        
        # Sector descriptions
        self.sector_descriptions = {
            "SILICON_VALLEY": "Where unicorns are born, and so are layoffs.",
            "TECH": "Where 'Junior' requires 10 years experience",
            "ACADEMIA": "Publish or perish (mostly perish)",
            "CREATIVE": "Exposure doesn't pay rent",
            "RETAIL": "Customer is always wrong, but smile anyway",
            # If you use enums, add: Sector.TECH: "...", etc.
        }
        
        # Initialize layer offsets for background
        self.background.create_placeholder_layers(self.sector)
        for layer in self.background.layers:
            layer["offset"] = 0
            
        # UI elements
        self.buzzword_rotation = ["Leverage", "Disrupt", "Paradigm Shift", "Synergy", "Agile"]
        self.current_buzzword = 0
        self.buzzword_timer = 0
        self.buzzword_interval = 2.0  # Seconds between buzzword changes
        
        # Coffee cup UI for stress meter
        self.coffee_cups = 5  # Start with full mental health
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # New attributes
        self.flash_timer = 0
        self.shake_timer = 0
        self.shake_offset = (0, 0)
        
    def reset_game(self):
        """Reset the game to initial state"""
        # Create player
        self.player = Player(self.sprite_manager, self.particle_system, self.lane_positions)
        self.player.set_sound_system(self.sound_system)
        self.player.game_ref = self  # Add this line
        
        # Create sprite groups
        self.obstacles = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        
        # Game variables
        self.speed = 200  # Initial speed
        self.obstacle_timer = 0
        self.power_up_timer = 0
        self.obstacle_interval = 2.0  # seconds
        self.power_up_interval = 5.0  # seconds
        
        # Job popup system
        self.job_popup_timer = 0
        self.job_popup_interval = 15.0  # seconds
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Calculate delta time
            current_time = time.time()
            self.delta_time = min(0.1, current_time - self.last_time)  # Cap delta time to prevent large jumps
            self.last_time = current_time
            
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(60)
            
        # Instead of quitting here, return a result
        return "quit"
        
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.GAME_OVER:
                        return False
                    
                if self.state == GameState.INTRO:
                    # Intro sequence handles its own events
                    pass
                elif self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                        self.sound_system.play_sound("button_click")
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = GameState.PLAYING
                        
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                        
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_UP:
                        self.player.change_lane("up")
                    elif event.key == pygame.K_DOWN:
                        self.player.change_lane("down")
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.player.slide()
                    elif event.key == pygame.K_e:
                        # Handle skill gap obstacle interaction
                        for obstacle in self.obstacles:
                            if obstacle.obstacle_type == "skill_gap" and obstacle.active:
                                if obstacle.handle_interaction(event.key):
                                    break
        return True
        
    def update(self):
        """Update game state"""
        # Update sound system
        self.sound_system.update()
        
        if self.state == GameState.INTRO:
            # Run intro sequence
            intro = IntroSequence(self.screen, self.clock, self.sound_system)
            self.player_name = intro.run()
            if self.player_name:  # Only proceed if we got a name
                self.state = GameState.MENU
            
        elif self.state == GameState.MENU:
            # Menu state - background music should be playing
            pass
            
        elif self.state == GameState.PLAYING:
            # When entering playing state, switch to Silicon Valley music
            if not hasattr(self, '_music_initialized'):
                self.sound_system.play_silicon_valley_music()
                self._music_initialized = True
            
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(self.delta_time, keys)
            
            # Update background
            for layer in self.background.layers:
                layer["offset"] = (layer["offset"] + self.speed * layer["speed"] * self.delta_time) % layer["surface"].get_width()
            # self.background.update_animated_layers(self.delta_time)
            
            # Update obstacles and power-ups
            for obstacle in self.obstacles:
                obstacle.update(self.delta_time, self.lane_positions)
                
            for power_up in self.power_ups:
                power_up.update(self.delta_time, self.lane_positions)
                
            # Update particles
            self.particle_system.update(self.delta_time)
            
            # Update popups
            self.popup_system.update(self.delta_time)
            
            # Spawn obstacles
            self.obstacle_timer += self.delta_time
            if self.obstacle_timer >= self.obstacle_interval:
                self.spawn_obstacle()
                self.obstacle_timer = 0
                
            # Spawn power-ups
            self.power_up_timer += self.delta_time
            if self.power_up_timer >= self.power_up_interval:
                self.spawn_power_up()
                self.power_up_timer = 0
                
            # Update job popup timer
            self.job_popup_timer += self.delta_time
            if self.job_popup_timer >= self.job_popup_interval:
                self.job_popup_timer = 0
                self.popup_system.show_job_posting()
                
            # Update buzzword rotation
            self.buzzword_timer += self.delta_time
            if self.buzzword_timer >= self.buzzword_interval:
                self.buzzword_timer = 0
                self.current_buzzword = (self.current_buzzword + 1) % len(self.buzzword_rotation)
                
            # Check collisions
            self.check_collisions()
            
            # Update score
            self.player.score += self.speed * self.delta_time * 0.01
            
            # Update speed based on score
            self.speed = 200 * (1 + (self.player.score // 100) * 0.05)
            
            # Check for sector transitions
            if self.player.score > self.sector_transition_score:
                old_sector = self.sector
                
                # Determine the next sector (example logic, adjust as needed)
                next_sector = None
                if self.sector == "SILICON_VALLEY":
                    next_sector = "TECH"
                elif self.sector == "TECH":
                    next_sector = "ACADEMIA"
                elif self.sector == "ACADEMIA":
                    next_sector = "CREATIVE"
                elif self.sector == "CREATIVE":
                    next_sector = "RETAIL"
                elif self.sector == "RETAIL":
                    next_sector = "SILICON_VALLEY"
                
                # Only transition if the next sector is different
                if next_sector and next_sector != self.sector:
                    self.sector = next_sector
                    self.popup_system.show_sector_transition(old_sector, self.sector)
                    self.background.create_placeholder_layers(self.sector)
                    for layer in self.background.layers:
                        layer["offset"] = 0
                    self.sector_transition_score += 500
                    self.sound_system.play_sound("sector_transition")
                    self.sound_system.play_bgm(self.sector)
                
            # Update coffee cups based on mental health
            self.coffee_cups = max(0, min(5, int(self.player.mental_health / 20)))
            
            # Game over condition
            if self.player.mental_health <= 0:
                self.state = GameState.GAME_OVER
                
        elif self.state == GameState.GAME_OVER:
            # Show game over screen
            game_over = GameOverScreen(self.screen, self.clock, self.player.score, self.sector_to_str(self.sector), self.player_name)
            result = game_over.run()
            if result == "restart":
                self.reset_game()
                self.state = GameState.PLAYING
            elif result == "quit":
                # Set a flag to break the main loop
                self._user_quit = True
                
    def spawn_obstacle(self):
        """Spawn a random obstacle"""
        obstacle_types = ["skill_gap", "ats_laser", "experience_wall", "burnout_cloud", "recruiter_bot"]
        weights = [0.25, 0.25, 0.2, 0.15, 0.15]  # Probability weights
        obstacle_type = random.choices(obstacle_types, weights=weights)[0]
        lane = random.randint(0, 2)
        
        new_obstacle = Obstacle(obstacle_type, lane, self.speed, self.sprite_manager, self.particle_system)
        new_obstacle.game_ref = self  # Add this line
        self.obstacles.add(new_obstacle)
        
    def spawn_power_up(self):
        """Spawn a random power-up"""
        power_up_types = ["nepotism_pass", "linkedin_premium", "mentorship_shield", "bootcamp_speed"]
        power_up_type = random.choice(power_up_types)
        lane = random.randint(0, 2)
        
        new_power_up = PowerUp(power_up_type, lane, self.speed, self.sprite_manager)
        self.power_ups.add(new_power_up)
        
    def check_collisions(self):
        """Check for collisions between player and game objects"""
        # Check obstacle collisions
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(self.player.rect) and obstacle.lane == self.player.current_lane:
                obstacle.active = True
                
                # If player has shield, destroy obstacle
                if self.player.has_mentorship_shield:
                    obstacle.kill()
                    self.player.add_score(50)
                    continue
                    
                # Handle burnout cloud and recruiter bot collisions immediately
                if obstacle.obstacle_type in ["burnout_cloud", "recruiter_bot"] and not obstacle.hit:
                    obstacle.hit = True
                    self.player.take_damage(obstacle.damage)
                    
            else:
                obstacle.active = False
                
            # Check recruiter bot projectile collisions
            if obstacle.obstacle_type == "recruiter_bot":
                for projectile in obstacle.projectiles:
                    if projectile.rect.colliderect(self.player.rect):
                        projectile.kill()
                        if not self.player.has_mentorship_shield:
                            self.player.take_damage(projectile.damage)
                
        # Check power-up collisions
        power_up_hits = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for power_up in power_up_hits:
            if power_up.lane == self.player.current_lane or self.player.has_nepotism_pass:
                self.player.activate_power_up(power_up.power_up_type)
                self.player.add_score(25)
                
    def draw(self):
        """Draw the game"""
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.INTRO:
            # Intro sequence handles its own drawing
            pass
            
        elif self.state == GameState.MENU:
            self.draw_menu()
            
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw background
            for i, layer in enumerate(self.background.layers):
                offset = int(layer["offset"])
                self.screen.blit(layer["surface"], (-offset, 0))
                self.screen.blit(layer["surface"], (layer["surface"].get_width() - offset, 0))
            
            # Draw lane dividers
            for i in range(1, 3):
                pygame.draw.line(self.screen, (255, 255, 255), 
                                (0, i * self.lane_height), 
                                (self.width, i * self.lane_height), 2)
                
            # Draw obstacles and power-ups
            for obstacle in self.obstacles:
                self.screen.blit(obstacle.image, obstacle.rect)
                
                # Draw recruiter bot projectiles
                if obstacle.obstacle_type == "recruiter_bot":
                    obstacle.draw_projectiles(self.screen)
                
            for power_up in self.power_ups:
                self.screen.blit(power_up.image, power_up.rect)
                
            # Draw player
            self.screen.blit(self.player.image, self.player.rect)
            
            # Draw particles
            self.particle_system.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Draw popups
            self.popup_system.draw(self.screen)
            
            # Draw pause screen if paused
            if self.state == GameState.PAUSED:
                self.draw_pause_screen()
                
        elif self.state == GameState.GAME_OVER:
            # Game over screen handles its own drawing
            pass
            
        # Update the display
        pygame.display.flip()
        
    def draw_menu(self):
        """Draw the main menu"""
        # Draw background
        for i, layer in enumerate(self.background.layers):
            offset = int(layer["offset"])
            self.screen.blit(layer["surface"], (-offset, 0))
            self.screen.blit(layer["surface"], (layer["surface"].get_width() - offset, 0))
        
        # Stronger semi-transparent overlay for better contrast
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))  # Increased alpha for more darkness
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_text = self.font_large.render("JOB RUSH 2025", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 3 - 60))
        
        # Subtitle
        subtitle_text = self.font_medium.render("THE JOB MARKET SIMULATOR NOBODY ASKED FOR", True, (255, 0, 0))
        self.screen.blit(subtitle_text, (self.width // 2 - subtitle_text.get_width() // 2, self.height // 3))
        
        # Player name with background box
        if self.player_name:
            name_text = self.font_large.render(f"Player: {self.player_name}", True, (0, 0, 0))
            name_bg_width = name_text.get_width() + 40
            name_bg_height = name_text.get_height() + 20
            name_bg_x = self.width // 2 - name_bg_width // 2
            name_bg_y = self.height // 3 + 70

            # Draw rounded rectangle background (or just a rect if you prefer)
            name_bg = pygame.Surface((name_bg_width, name_bg_height), pygame.SRCALPHA)
            name_bg.fill((255, 255, 255, 220))  # White with some transparency
            self.screen.blit(name_bg, (name_bg_x, name_bg_y))

            # Draw the player name in bold/dark text for contrast
            name_text = self.font_large.render(f"Player: {self.player_name}", True, (30, 30, 30))
            self.screen.blit(name_text, (self.width // 2 - name_text.get_width() // 2, name_bg_y + 10))
        
        # Instructions (with more spacing)
        instructions = [
            "Arrow Keys: Change Lane",
            "Space: Jump",
            "Ctrl: Slide",
            "E: Interact with Skill Gap",
            "WASD: Match ATS Laser Patterns",
            "Click: Break Experience Wall",
            "P: Pause Game",
            "Press SPACE to Start"
        ]
        instruction_y = self.height // 2 + 60
        for instruction in instructions:
            instruction_text = self.font_small.render(instruction, True, (255, 255, 255))
            self.screen.blit(instruction_text, (self.width // 2 - instruction_text.get_width() // 2, instruction_y))
            instruction_y += 36  # More vertical space
            
    def draw_ui(self):
        """Draw the game UI"""
        # Draw mental health as coffee cups
        for i in range(5):
            if i < self.coffee_cups:
                cup_image = self.sprite_manager.get_sprite("coffee_cup")
                self.sound_system.play_sound("coffee_cup")
            else:
                cup_image = self.sprite_manager.get_sprite("empty_cup")
            self.screen.blit(cup_image, (20 + i * 25, 20))
            
        # Draw mental health text
        health_text = self.font_small.render(f"Mental Health: {int(self.player.mental_health)}", True, (255, 255, 255))
        self.screen.blit(health_text, (20, 50))
        
        # Draw score with rotating buzzword
        score_text = self.font_medium.render(f"{self.buzzword_rotation[self.current_buzzword]} Points: {int(self.player.score)}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.width - score_text.get_width() - 20, 20))
        
        # Draw sector banner with auto-wrapping and dynamic height
        banner_width = 400
        desc = self.sector_descriptions.get(self.sector)
        if desc is None and hasattr(self.sector, "name"):
            desc = self.sector_descriptions.get(self.sector.name)
        if desc is None:
            desc = "Welcome to the job market!"

        desc_font = pygame.font.Font(None, 20)
        max_width = banner_width - 20
        desc_lines = []
        line = ""
        for word in desc.split():
            test_line = f"{line} {word}".strip()
            if desc_font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                desc_lines.append(line)
                line = word
        if line:
            desc_lines.append(line)

        banner_height = 30 + 20 * len(desc_lines)
        banner_x = self.width // 2 - banner_width // 2
        banner_y = 10
        banner_rect = pygame.Rect(banner_x, banner_y, banner_width, banner_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), banner_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), banner_rect, 2, border_radius=10)

        sector_str = self.sector if isinstance(self.sector, str) else getattr(self.sector, "name", str(self.sector))
        sector_text = self.font_medium.render(f"SECTOR: {sector_str}", True, (255, 255, 255))
        self.screen.blit(sector_text, (banner_x + 10, banner_y + 5))

        for i, line in enumerate(desc_lines):
            desc_surface = desc_font.render(line, True, (255, 0, 0))
            self.screen.blit(desc_surface, (banner_x + 10, banner_y + 30 + i * 20))

        # Draw active power-ups
        power_up_y = 80
        if self.player.has_nepotism_pass:
            power_up_text = self.font_small.render("Nepotism Pass Active!", True, (255, 215, 0))
            self.screen.blit(power_up_text, (20, power_up_y))
            power_up_y += 25
        if self.player.has_linkedin_premium:
            power_up_text = self.font_small.render("LinkedIn Premium Active!", True, (0, 119, 181))
            self.screen.blit(power_up_text, (20, power_up_y))
            power_up_y += 25
        if self.player.has_mentorship_shield:
            power_up_text = self.font_small.render("Mentorship Shield Active!", True, (0, 255, 0))
            self.screen.blit(power_up_text, (20, power_up_y))
            power_up_y += 25
        if self.player.has_bootcamp_speed:
            power_up_text = self.font_small.render("Bootcamp Speed Active!", True, (255, 255, 0))
            self.screen.blit(power_up_text, (20, power_up_y))
        
    def draw_pause_screen(self):
        """Draw the pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(pause_text, (self.width // 2 - pause_text.get_width() // 2, self.height // 3))
        
        # Resume instructions
        resume_text = self.font_medium.render("Press P to Resume", True, (255, 255, 255))
        self.screen.blit(resume_text, (self.width // 2 - resume_text.get_width() // 2, self.height // 2))
        
        # Quit instructions
        quit_text = self.font_small.render("Press ESC to Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, (self.width // 2 - quit_text.get_width() // 2, self.height // 2 + 50))

    def sector_to_str(self, sector):
        return sector.name if hasattr(sector, "name") else str(sector)

    def update_shake_flash(self):
        if self.flash_timer > 0:
            self.flash_timer -= self.delta_time
        if self.shake_timer > 0:
            self.shake_timer -= self.delta_time
            self.shake_offset = (random.randint(-6, 6), random.randint(-6, 6))
        else:
            self.shake_offset = (0, 0)

    def trigger_shake_flash(self):
        self.flash_timer = 0.18
        self.shake_timer = 0.18
