#!/usr/bin/env python3
import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type, lane, speed, sprite_manager, particle_system):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.lane = lane
        self.speed = speed
        self.sprite_manager = sprite_manager
        self.particle_system = particle_system
        
        # Set up obstacle based on type
        if obstacle_type == "skill_gap":
            self.image = self.sprite_manager.get_sprite("skill_gap")
            self.qte_count = 3
            self.qte_key = pygame.K_e
            self.damage = 15
        elif obstacle_type == "ats_laser":
            self.image = self.sprite_manager.get_sprite("ats_laser")
            self.pattern = self.generate_pattern()
            self.current_pattern_index = 0
            self.damage = 20
        elif obstacle_type == "experience_wall":
            self.image = self.sprite_manager.get_sprite("experience_wall")
            self.click_count = 0
            self.required_clicks = 5
            self.damage = 25
        elif obstacle_type == "burnout_cloud":
            self.image = self.sprite_manager.get_sprite("burnout_cloud")
            self.damage = 30
        elif obstacle_type == "recruiter_bot":
            self.image = self.sprite_manager.get_sprite("recruiter_bot")
            self.damage = 10
            self.shoot_timer = 0
            self.shoot_interval = 1.0  # Seconds between shots
            self.projectiles = pygame.sprite.Group()
        
        self.rect = self.image.get_rect()
        self.rect.x = 1280  # Start off-screen to the right
        self.rect.centery = 0  # Will be set in update
        self.active = False
        self.hit = False  # Whether the obstacle has been hit by the player
        
        # Visual effects
        self.flash_timer = 0
        self.flash_duration = 0.1
        self.is_flashing = False
        
        self.game_ref = None  # Will be set by Game after creation
        
    def update(self, delta_time, lane_positions):
        self.rect.x -= self.speed * delta_time
        
        # Set vertical position based on lane
        self.rect.centery = lane_positions[self.lane]
        
        # Handle recruiter bot projectiles
        if self.obstacle_type == "recruiter_bot":
            self.shoot_timer += delta_time
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                self.shoot_projectile()
                
            # Update projectiles
            for projectile in self.projectiles:
                projectile.update(delta_time)
                if projectile.rect.right < 0:
                    projectile.kill()
                    
        # Handle flashing effect when hit
        if self.is_flashing:
            self.flash_timer += delta_time
            if self.flash_timer >= self.flash_duration:
                self.is_flashing = False
                self.flash_timer = 0
                # Restore original image
                if self.obstacle_type == "skill_gap":
                    self.image = self.sprite_manager.get_sprite("skill_gap")
                elif self.obstacle_type == "ats_laser":
                    self.image = self.sprite_manager.get_sprite("ats_laser")
                elif self.obstacle_type == "experience_wall":
                    self.image = self.sprite_manager.get_sprite("experience_wall")
                elif self.obstacle_type == "burnout_cloud":
                    self.image = self.sprite_manager.get_sprite("burnout_cloud")
                elif self.obstacle_type == "recruiter_bot":
                    self.image = self.sprite_manager.get_sprite("recruiter_bot")
            
        # Remove if off screen
        if self.rect.right < 0:
            self.kill()
            
    def generate_pattern(self):
        # Generate a random WASD pattern
        keys = ["w", "a", "s", "d"]
        return [random.choice(keys) for _ in range(4)]
    
    def handle_interaction(self, key):
        if not self.active:
            return False
            
        if self.obstacle_type == "skill_gap":
            if key == self.qte_key:
                self.qte_count -= 1
                self.flash()
                self.particle_system.add_stress_particles(self.rect.centerx, self.rect.centery, 2)
                if self.game_ref:
                    self.game_ref.sound_system.play_sound("skill_gap")
                if self.qte_count <= 0:
                    return True
        elif self.obstacle_type == "ats_laser":
            pattern_key = self.pattern[self.current_pattern_index]
            if (pattern_key == "w" and key == pygame.K_w) or \
               (pattern_key == "a" and key == pygame.K_a) or \
               (pattern_key == "s" and key == pygame.K_s) or \
               (pattern_key == "d" and key == pygame.K_d):
                self.current_pattern_index += 1
                self.flash()
                self.particle_system.add_stress_particles(self.rect.centerx, self.rect.centery, 2)
                if self.game_ref:
                    self.game_ref.sound_system.play_sound("ats_laser")
                if self.current_pattern_index >= len(self.pattern):
                    return True
            else:
                # Reset pattern on mistake
                self.current_pattern_index = 0
                self.particle_system.add_stress_particles(self.rect.centerx, self.rect.centery, 5)
        
        return False
        
    def handle_click(self):
        if self.obstacle_type == "experience_wall" and self.active:
            self.click_count += 1
            self.flash()
            self.particle_system.add_stress_particles(self.rect.centerx, self.rect.centery, 2)
            if self.game_ref:
                self.game_ref.sound_system.play_sound("experience_wall")
            if self.click_count >= self.required_clicks:
                return True
        return False
        
    def flash(self):
        """Create a flash effect when the obstacle is hit"""
        self.is_flashing = True
        self.flash_timer = 0
        
        # Create a white version of the image
        if self.obstacle_type == "skill_gap":
            flash_image = self.sprite_manager.get_sprite("skill_gap").copy()
        elif self.obstacle_type == "ats_laser":
            flash_image = self.sprite_manager.get_sprite("ats_laser").copy()
        elif self.obstacle_type == "experience_wall":
            flash_image = self.sprite_manager.get_sprite("experience_wall").copy()
        elif self.obstacle_type == "burnout_cloud":
            flash_image = self.sprite_manager.get_sprite("burnout_cloud").copy()
        elif self.obstacle_type == "recruiter_bot":
            flash_image = self.sprite_manager.get_sprite("recruiter_bot").copy()
            
        # Apply white tint
        white_overlay = pygame.Surface(flash_image.get_size(), pygame.SRCALPHA)
        white_overlay.fill((255, 255, 255, 128))
        flash_image.blit(white_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        self.image = flash_image
        
    def shoot_projectile(self):
        """Recruiter bot shoots an unpaid internship projectile"""
        projectile = Projectile(
            self.rect.left, 
            self.rect.centery, 
            self.speed * 1.5,
            self.sprite_manager.get_sprite("unpaid_projectile")
        )
        self.projectiles.add(projectile)
        
    def draw_projectiles(self, surface):
        """Draw recruiter bot projectiles"""
        if self.obstacle_type == "recruiter_bot":
            for projectile in self.projectiles:
                surface.blit(projectile.image, projectile.rect)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.speed = speed
        self.damage = 10
        
    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, lane, speed, sprite_manager):
        super().__init__()
        self.power_up_type = power_up_type
        self.lane = lane
        self.speed = speed
        self.sprite_manager = sprite_manager
        
        # Set up power-up based on type
        if power_up_type == "nepotism_pass":
            self.image = self.sprite_manager.get_sprite("nepotism_pass")
        elif power_up_type == "linkedin_premium":
            self.image = self.sprite_manager.get_sprite("linkedin_premium")
        elif power_up_type == "mentorship_shield":
            self.image = self.sprite_manager.get_sprite("mentorship_shield")
        elif power_up_type == "bootcamp_speed":
            self.image = self.sprite_manager.get_sprite("bootcamp_speed")
            
        self.rect = self.image.get_rect()
        self.rect.x = 1280  # Start off-screen to the right
        self.rect.centery = 0  # Will be set in update
        
        # Animation
        self.float_offset = 0
        self.float_speed = 2
        self.float_direction = 1
        
    def update(self, delta_time, lane_positions):
        self.rect.x -= self.speed * delta_time
        
        # Set vertical position based on lane with floating animation
        self.float_offset += self.float_speed * self.float_direction * delta_time
        if abs(self.float_offset) > 10:
            self.float_direction *= -1
            
        self.rect.centery = lane_positions[self.lane] + self.float_offset
        
        # Remove if off screen
        if self.rect.right < 0:
            self.kill()
