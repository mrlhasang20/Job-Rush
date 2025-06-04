#!/usr/bin/env python3
import pygame
import random
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_manager, particle_system, lane_positions):
        super().__init__()
        self.sprite_manager = sprite_manager
        self.particle_system = particle_system
        self.lane_positions = lane_positions
        self.current_lane = 1  # Start in the middle lane
        
        # Load player sprites
        self.animations = sprite_manager.animations
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.bottom = 600  # Adjust as needed for your ground level
        
        # Animation state
        self.state = "idle"
        self.frame = 0
        self.frame_timer = 0
        self.animation_speed = 0.1  # Time between frames in seconds
        
        # Physics
        self.velocity_y = 0
        self.gravity = 1200  # pixels/sec^2
        self.jump_power = 600
        self.is_jumping = False
        self.is_sliding = False
        self.slide_timer = 0
        
        # Player states
        self.mental_health = 100
        self.score = 0
        self.skills_collected = 0
        self.coffee_consumed = 0
        self.buzzwords_learned = 0
        self.dreams_crushed = 0
        self.years_experience_faked = 0
        
        # Power-up states
        self.has_nepotism_pass = False
        self.has_linkedin_premium = False
        self.has_mentorship_shield = False
        self.has_bootcamp_speed = False
        self.power_up_timer = 0
        
        # Anxiety spark timer
        self.anxiety_timer = 0
        
        # New attributes
        self.flash_timer = 0.18
        self.shake_timer = 0.18
        self.shake_offset = (0, 0)
        
        # Sound system reference
        self.sound_system = None  # Will be set by Game after creation

    def set_sound_system(self, sound_system):
        """Set the sound system reference"""
        self.sound_system = sound_system

    def update(self, dt, keys):
        # Handle input
        if not self.is_jumping and not self.is_sliding and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.velocity_y = -self.jump_power
        if not self.is_jumping and not self.is_sliding and keys[pygame.K_LCTRL]:
            self.is_sliding = True
            self.slide_timer = 0.5  # Slide for 0.5 seconds

        # Physics
        if self.is_jumping:
            self.velocity_y += self.gravity * dt
            self.rect.y += int(self.velocity_y * dt)
            if self.rect.bottom >= 600:  # Ground level
                self.rect.bottom = 600
                self.is_jumping = False
                self.velocity_y = 0

        if self.is_sliding:
            self.slide_timer -= dt
            if self.slide_timer <= 0:
                self.is_sliding = False

        # Update lane position
        target_y = self.lane_positions[self.current_lane]
        if self.rect.centery < target_y:
            self.rect.centery = min(self.rect.centery + 10, target_y)
        elif self.rect.centery > target_y:
            self.rect.centery = max(self.rect.centery - 10, target_y)

        # Animation state
        if self.is_jumping:
            self.state = "jump"
        elif self.is_sliding:
            self.state = "slide"
        else:
            self.state = "run"  # Or "idle" if you want idle when not moving

        # Animation frame update
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % len(self.animations[self.state])
            self.frame_timer = 0
            self.image = self.animations[self.state][self.frame]
        
        # Handle power-ups
        if self.has_bootcamp_speed:
            self.mental_health -= 5 * dt
            
            # Add anxiety particles occasionally
            if random.random() < 0.2:
                self.particle_system.add_anxiety_sparks(self.rect.centerx, self.rect.centery, 2)
            
        if self.power_up_timer > 0:
            self.power_up_timer -= dt
            if self.power_up_timer <= 0:
                self.has_nepotism_pass = False
                self.has_linkedin_premium = False
                self.has_mentorship_shield = False
                self.has_bootcamp_speed = False
                
        # Anxiety sparks when mental health is low
        self.anxiety_timer += dt
        if self.anxiety_timer >= 0.5 and self.mental_health < 30:
            self.anxiety_timer = 0
            self.particle_system.add_anxiety_sparks(self.rect.centerx, self.rect.centery, 3)
            if self.sound_system:
                self.sound_system.play_sound("anxiety_sparks")
                
        # Clamp mental health
        self.mental_health = max(0, min(100, self.mental_health))
        
        # At the end of update (after all other updates)
        if self.flash_timer > 0:
            self.flash_timer -= dt
        if self.shake_timer > 0:
            self.shake_timer -= dt
            self.shake_offset = (random.randint(-6, 6), random.randint(-6, 6))
        else:
            self.shake_offset = (0, 0)
        
    def change_lane(self, direction):
        """Change the player's lane"""
        if direction == "up" and self.current_lane > 0:
            self.current_lane -= 1
            if self.sound_system:
                self.sound_system.play_sound("lane_change")
        elif direction == "down" and self.current_lane < 2:
            self.current_lane += 1
            if self.sound_system:
                self.sound_system.play_sound("lane_change")
            
    def jump(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_jumping = True
            self.velocity_y = self.jump_power
            if self.sound_system:
                self.sound_system.play_sound("jump")
            
    def slide(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_sliding = True
            if self.sound_system:
                self.sound_system.play_sound("slide")
            # Start slide animation and hitbox change
            
    def end_slide(self):
        self.is_sliding = False
        # Reset hitbox and animation
        
    def activate_power_up(self, power_up_type):
        self.power_up_timer = 10
        if self.sound_system:
            self.sound_system.play_sound(power_up_type)
        
        if power_up_type == "nepotism_pass":
            self.has_nepotism_pass = True
            # Add money particles
            self.particle_system.add_money_particles(self.rect.centerx, self.rect.centery, 15)
        elif power_up_type == "linkedin_premium":
            self.has_linkedin_premium = True
            # Add diploma particles
            self.particle_system.add_diploma_particles(self.rect.centerx, self.rect.centery, 10)
        elif power_up_type == "mentorship_shield":
            self.has_mentorship_shield = True
        elif power_up_type == "bootcamp_speed":
            self.has_bootcamp_speed = True
            
    def take_damage(self, amount):
        """Take mental health damage and show stress particles"""
        if self.has_mentorship_shield:
            # Reduced damage with shield
            self.mental_health -= amount * 0.2
        else:
            self.mental_health -= amount
            
        # Add stress particles
        self.particle_system.add_stress_particles(self.rect.centerx, self.rect.centery, int(amount))
        
        # Increment dreams crushed
        self.dreams_crushed += 1
        
        if self.sound_system:
            self.sound_system.flash_timer = 0.18  # seconds
            self.sound_system.shake_timer = 0.18  # seconds
        
    def gain_health(self, amount):
        """Gain mental health"""
        self.mental_health = min(100, self.mental_health + amount)
        
    def add_score(self, amount):
        """Add to score and related stats"""
        self.score += amount
        
        # Update related stats
        self.years_experience_faked = int(self.score / 100)
        self.buzzwords_learned = int(self.score / 50)
        self.coffee_consumed += amount * 0.01
