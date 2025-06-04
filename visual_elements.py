#!/usr/bin/env python3
import pygame
import os
import random
import math
import textwrap

class SpriteManager:
    def __init__(self):
        """Initialize sprite manager with placeholder sprites"""
        self.sprites = {}
        self.animations = {
            "run": self.load_animation("assets/player/run"),
            "jump": self.load_animation("assets/player/jump"),
            "slide": self.load_animation("assets/player/slide"),
            "idle": self.load_animation("assets/player/idle"),
        }
        
        # Create placeholder sprites
        self.create_placeholder_sprites()
        self.flash_timer = 0
        self.shake_timer = 0
        self.shake_offset = (0, 0)
        
    def create_placeholder_sprites(self):
        """Create placeholder sprites until real assets are available"""
        # Player sprite (simple human figure with cap and briefcase)
        player_sprite = pygame.Surface((50, 70), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(player_sprite, (0, 100, 255), (20, 30, 10, 30))  # Torso
        # Head
        pygame.draw.circle(player_sprite, (255, 224, 189), (25, 20), 10)  # Head (skin color)
        # Arms
        pygame.draw.line(player_sprite, (0, 100, 255), (25, 40), (10, 55), 5)  # Left arm
        pygame.draw.line(player_sprite, (0, 100, 255), (25, 40), (40, 55), 5)  # Right arm
        # Legs
        pygame.draw.line(player_sprite, (0, 0, 0), (25, 60), (15, 70), 5)  # Left leg
        pygame.draw.line(player_sprite, (0, 0, 0), (25, 60), (35, 70), 5)  # Right leg
        # Cap
        pygame.draw.polygon(player_sprite, (0, 0, 0), [(15, 13), (35, 13), (25, 7)])  # Cap top
        pygame.draw.line(player_sprite, (0, 0, 0), (25, 13), (25, 20), 2)  # Cap tassel
        # Briefcase
        pygame.draw.rect(player_sprite, (139, 69, 19), (35, 50, 10, 10))  # Briefcase
        pygame.draw.rect(player_sprite, (0, 0, 0), (35, 50, 10, 10), 1)  # Briefcase outline
        self.sprites["player"] = player_sprite
        
        # Player animations
        self.animations["player_run"] = [player_sprite]  # Just one frame for now
        
        player_jump = player_sprite.copy()
        pygame.draw.rect(player_jump, (0, 100, 255), (0, 10, 50, 50))  # Body higher up
        pygame.draw.polygon(player_jump, (0, 0, 0), [(0, 10), (50, 10), (25, -10)])  # Cap
        pygame.draw.rect(player_jump, (139, 69, 19), (10, 30, 30, 20))  # Briefcase
        self.animations["player_jump"] = [player_jump]
        
        player_slide = pygame.Surface((70, 40), pygame.SRCALPHA)
        pygame.draw.rect(player_slide, (0, 100, 255), (0, 10, 70, 30))  # Body stretched
        pygame.draw.polygon(player_slide, (0, 0, 0), [(50, 10), (70, 10), (60, 0)])  # Cap
        pygame.draw.rect(player_slide, (139, 69, 19), (10, 15, 30, 20))  # Briefcase
        self.animations["player_slide"] = [player_slide]
        
        # Obstacles
        # ATS Laser
        ats_laser = pygame.Surface((100, 60), pygame.SRCALPHA)
        pygame.draw.rect(ats_laser, (255, 0, 0, 180), (0, 0, 100, 60))
        font = pygame.font.Font(None, 20)
        text = font.render("RESUME REJECTED", True, (255, 255, 255))
        ats_laser.blit(text, (5, 20))
        self.sprites["ats_laser"] = ats_laser
        
        # Skill Gap (triangle with readable label)
        skill_gap = pygame.Surface((80, 40), pygame.SRCALPHA)
        pygame.draw.polygon(skill_gap, (255, 0, 0), [(0, 40), (80, 40), (40, 0)])
        font = pygame.font.Font(None, 20)
        # Add background for text
        text_bg = pygame.Surface((76, 20), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 180))
        skill_gap.blit(text_bg, (2, 10))
        text = font.render("5+ YRS EXP", True, (255, 255, 255))
        skill_gap.blit(text, (6, 12))
        self.sprites["skill_gap"] = skill_gap
        
        # Experience Wall (with readable label)
        exp_wall = pygame.Surface((60, 80), pygame.SRCALPHA)
        for y in range(0, 80, 20):
            for x in range(0, 60, 30):
                pygame.draw.rect(exp_wall, (139, 69, 19), (x, y, 28, 18))
                pygame.draw.rect(exp_wall, (0, 0, 0), (x, y, 28, 18), 1)
        font = pygame.font.Font(None, 18)
        text_bg = pygame.Surface((56, 20), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 180))
        exp_wall.blit(text_bg, (2, 30))
        text = font.render("PhD REQ", True, (255, 255, 255))
        exp_wall.blit(text, (8, 32))
        self.sprites["experience_wall"] = exp_wall
        
        # Burnout Cloud
        burnout_cloud = pygame.Surface((70, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(burnout_cloud, (100, 100, 100, 200), (0, 10, 40, 30))
        pygame.draw.ellipse(burnout_cloud, (80, 80, 80, 200), (20, 0, 50, 40))
        pygame.draw.ellipse(burnout_cloud, (60, 60, 60, 200), (30, 10, 40, 30))
        # Lightning bolt
        pygame.draw.polygon(burnout_cloud, (255, 255, 0), [(40, 10), (30, 25), (40, 25), (30, 40)])
        self.sprites["burnout_cloud"] = burnout_cloud
        
        # Recruiter Bot
        recruiter_bot = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.rect(recruiter_bot, (150, 150, 150), (10, 10, 40, 40))  # Body
        pygame.draw.rect(recruiter_bot, (200, 200, 200), (15, 15, 30, 20))  # Screen
        pygame.draw.rect(recruiter_bot, (255, 0, 0), (20, 20, 5, 5))  # Eye
        pygame.draw.rect(recruiter_bot, (255, 0, 0), (35, 20, 5, 5))  # Eye
        pygame.draw.rect(recruiter_bot, (0, 0, 0), (20, 30, 20, 5))  # Mouth
        pygame.draw.rect(recruiter_bot, (100, 100, 100), (0, 25, 10, 20))  # Arm
        pygame.draw.rect(recruiter_bot, (100, 100, 100), (50, 25, 10, 20))  # Arm
        self.sprites["recruiter_bot"] = recruiter_bot
        
        # Unpaid Internship Projectile
        projectile = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(projectile, (255, 0, 0), (0, 0, 40, 20))
        font = pygame.font.Font(None, 12)
        text = font.render("UNPAID", True, (255, 255, 255))
        projectile.blit(text, (2, 5))
        self.sprites["unpaid_projectile"] = projectile
        
        # Power-ups
        # Nepotism Pass
        nepotism = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(nepotism, (255, 215, 0), (15, 15), 15)  # Golden circle
        pygame.draw.polygon(nepotism, (255, 255, 255), [(15, 0), (10, 10), (20, 10)])  # Crown
        pygame.draw.line(nepotism, (0, 0, 0), (10, 20), (20, 20), 2)  # Handshake
        self.sprites["nepotism_pass"] = nepotism
        
        # LinkedIn Premium
        linkedin = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(linkedin, (0, 119, 181), (15, 15), 15)  # LinkedIn blue
        pygame.draw.circle(linkedin, (255, 255, 255), (15, 15), 12)  # White inner circle
        pygame.draw.circle(linkedin, (0, 119, 181), (15, 15), 10)  # Blue inner circle
        font = pygame.font.Font(None, 14)
        text = font.render("in", True, (255, 255, 255))
        linkedin.blit(text, (11, 9))
        self.sprites["linkedin_premium"] = linkedin
        
        # Mentorship Shield
        mentorship = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(mentorship, (0, 255, 0), [(15, 0), (30, 10), (25, 25), (15, 30), (5, 25), (0, 10)])
        pygame.draw.circle(mentorship, (255, 255, 255), (15, 12), 8)  # Face
        pygame.draw.circle(mentorship, (0, 0, 0), (12, 10), 2)  # Eye
        pygame.draw.circle(mentorship, (0, 0, 0), (18, 10), 2)  # Eye
        pygame.draw.arc(mentorship, (0, 0, 0), (10, 12, 10, 8), 0, 3.14, 1)  # Smile
        self.sprites["mentorship_shield"] = mentorship
        
        # Bootcamp Speed
        bootcamp = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(bootcamp, (255, 255, 0), [(0, 15), (15, 0), (15, 10), (30, 10), (15, 30), (15, 20), (0, 20)])
        font = pygame.font.Font(None, 10)
        text = font.render("SPEED", True, (0, 0, 0))
        bootcamp.blit(text, (5, 12))
        self.sprites["bootcamp_speed"] = bootcamp
        
        # UI Elements
        # Coffee cup for stress meter
        coffee_cup = pygame.Surface((20, 25), pygame.SRCALPHA)
        pygame.draw.rect(coffee_cup, (139, 69, 19), (3, 5, 14, 15))  # Cup
        pygame.draw.ellipse(coffee_cup, (139, 69, 19), (3, 0, 14, 10))  # Top
        pygame.draw.ellipse(coffee_cup, (101, 67, 33), (5, 5, 10, 5))  # Coffee
        pygame.draw.rect(coffee_cup, (139, 69, 19), (17, 8, 3, 5))  # Handle
        self.sprites["coffee_cup"] = coffee_cup
        
        # Empty coffee cup
        empty_cup = coffee_cup.copy()
        pygame.draw.line(empty_cup, (255, 0, 0), (0, 0), (20, 25), 2)
        self.sprites["empty_cup"] = empty_cup
        
    def get_sprite(self, name):
        """Get a sprite by name"""
        if name in self.sprites:
            return self.sprites[name]
        else:
            # Return a default error sprite
            error_sprite = pygame.Surface((30, 30))
            error_sprite.fill((255, 0, 255))  # Magenta for missing sprites
            return error_sprite
            
    def get_animation_frame(self, name, frame_index):
        """Get a specific frame from an animation"""
        if name in self.animations:
            frames = self.animations[name]
            if frames:
                return frames[frame_index % len(frames)]
        
        # Return default sprite if animation not found
        return self.get_sprite("player")

    def load_animation(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                frames.append(pygame.image.load(os.path.join(folder, filename)).convert_alpha())
        return frames

    def get_animation(self, state):
        return self.animations[state]

class ParallaxBackground:
    def __init__(self, screen_width, screen_height, sector):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layers = []
        self.billboard_offset = 0
        self.window_flicker_state = {}
        self.drone_positions = []
        self.create_placeholder_layers(sector)
        
    def load_logo(self, name):
        path = os.path.join("assets", "logos", f"{name}.png")
        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha()
        else:
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.rect(surf, (200, 200, 200), (0, 0, 40, 40))
            font = pygame.font.Font(None, 18)
            text = font.render(name[0].upper(), True, (0, 0, 0))
            surf.blit(text, (10, 10))
            return surf

    def create_skyline_layer(self, sector_key):
        layer = pygame.Surface((self.screen_width * 2, self.screen_height), pygame.SRCALPHA)
        if sector_key == "SILICON_VALLEY":
            color = (120, 220, 200)
            for x in range(0, self.screen_width * 2, 180):
                height = random.randint(100, 180)
                pygame.draw.rect(layer, color, (x, self.screen_height - height, 140, height), border_radius=18)
                # Solar panels
                pygame.draw.rect(layer, (80, 120, 120), (x+20, self.screen_height - height + 20, 40, 10))
        elif sector_key == "TECH":
            color = (60, 60, 100)
            for x in range(0, self.screen_width * 2, 140):
                height = random.randint(120, 200)
                pygame.draw.rect(layer, color, (x, self.screen_height - height, 100, height), border_radius=8)
                # Server lights
                for i in range(5):
                    pygame.draw.circle(layer, (0, 255, 0), (x+20+i*15, self.screen_height - height + 20), 3)
        elif sector_key == "ACADEMIA":
            color = (180, 180, 140)
            for x in range(0, self.screen_width * 2, 200):
                height = random.randint(130, 180)
                pygame.draw.rect(layer, color, (x, self.screen_height - height, 120, height), border_radius=12)
                # Clock tower
                pygame.draw.rect(layer, (120, 120, 100), (x+40, self.screen_height - height - 40, 40, 40))
                pygame.draw.circle(layer, (255, 255, 255), (x+60, self.screen_height - height - 20), 12)
        elif sector_key == "CREATIVE":
            for x in range(0, self.screen_width * 2, 160):
                height = random.randint(100, 180)
                color = (random.randint(180, 255), random.randint(100, 200), random.randint(180, 255))
                pygame.draw.rect(layer, color, (x, self.screen_height - height, 120, height), border_radius=20)
                # Spotlights
                pygame.draw.polygon(layer, (255, 255, 180, 80), [
                    (x+60, self.screen_height - height),
                    (x+40, self.screen_height),
                    (x+80, self.screen_height)
                ])
        elif sector_key == "RETAIL":
            color = (200, 200, 200)
            for x in range(0, self.screen_width * 2, 180):
                height = random.randint(100, 160)
                pygame.draw.rect(layer, color, (x, self.screen_height - height, 140, height), border_radius=10)
                # Sale sign
                pygame.draw.rect(layer, (255, 0, 0), (x+30, self.screen_height - height + 30, 40, 20))
                font = pygame.font.Font(None, 18)
                text = font.render("SALE", True, (255, 255, 255))
                layer.blit(text, (x+35, self.screen_height - height + 32))
        else:
            color = (50, 50, 70)
            for x in range(0, self.screen_width * 2, 120):
                height = random.randint(120, 220)
                pygame.draw.rect(layer, color, (x, self.screen_height - height, 100, height))
        return {"surface": layer, "speed": 0.08, "offset": 0}

    def create_cloud_layer(self, sector_key):
        layer = pygame.Surface((self.screen_width * 2, self.screen_height), pygame.SRCALPHA)
        if sector_key == "SILICON_VALLEY":
            # Silicon Valley clouds
            for _ in range(8):
                x = random.randint(0, self.screen_width * 2)
                y = random.randint(30, 250)
                size = random.randint(100, 200)
                cloud = pygame.Surface((size, size // 2), pygame.SRCALPHA)
                for i in range(3):
                    pygame.draw.ellipse(cloud, (220, 220, 220, 120), (i*size//8, i*size//12, size//2, size//3))
                layer.blit(cloud, (x, y))
        else:
            # Other sectors' clouds
            for _ in range(12):
                x = random.randint(0, self.screen_width * 2)
                y = random.randint(30, 250)
                size = random.randint(80, 180)
                cloud = pygame.Surface((size, size // 2), pygame.SRCALPHA)
                for i in range(3):
                    pygame.draw.ellipse(cloud, (220, 220, 220, 120), (i*size//8, i*size//12, size//2, size//3))
                layer.blit(cloud, (x, y))
        return {"surface": layer, "speed": 0.15, "offset": 0}

    def create_building_layer(self, sector):
        layer = pygame.Surface((self.screen_width * 2, self.screen_height), pygame.SRCALPHA)
        y_base = self.screen_height

        # Randomized buildings
        building_colors = [(70, 70, 90), (100, 100, 120), (120, 120, 140)]
        num_buildings = self.screen_width * 2 // 80
        company_buildings = random.sample(range(num_buildings), min(4, num_buildings))

        # Sector-specific companies
        companies = {
            "SILICON_VALLEY": [
                {"name": "Google", "logo": "google"},
                {"name": "Apple", "logo": "apple"},
                {"name": "Meta", "logo": "meta"},
                {"name": "Netflix", "logo": "netflix"},
                {"name": "StartupX", "logo": "startupx"},
                {"name": "ChatGPT", "logo": "chatgpt"},
            ],
            "TECH": [
                {"name": "Amazon", "logo": "amazon"},
                {"name": "Microsoft", "logo": "microsoft"},
                {"name": "IBM", "logo": "ibm"},
                {"name": "Oracle", "logo": "oracle"},
            ],
            "ACADEMIA": [
                {"name": "Harvard", "logo": "harvard"},
                {"name": "MIT", "logo": "mit"},
                {"name": "Stanford", "logo": "stanford"},
                {"name": "Library", "logo": "library"},
            ],
            "CREATIVE": [
                {"name": "ArtStudio", "logo": "artstudio"},
                {"name": "Theater", "logo": "theater"},
                {"name": "Gallery", "logo": "gallery"},
            ],
            "RETAIL": [
                {"name": "Mall", "logo": "mall"},
                {"name": "ShopEZ", "logo": "shopez"},
                {"name": "SuperMart", "logo": "supermart"},
            ]
        }
        sector_key = str(sector).upper()
        sector_companies = companies.get(sector_key, [])
        company_idx = 0

        for i in range(num_buildings):
            x = i * 80 + random.randint(-10, 10)
            width = random.randint(60, 90)
            height = random.randint(180, 320)
            color = random.choice(building_colors)
            pygame.draw.rect(layer, color, (x, y_base - height, width, height), border_radius=8)

            # Place a company billboard on a few buildings
            if i in company_buildings and company_idx < len(sector_companies):
                logo = self.load_logo(sector_companies[company_idx]["logo"])
                logo = pygame.transform.smoothscale(logo, (40, 40))
                billboard_rect = pygame.Rect(x + width // 2 - 20, y_base - height - 50, 40, 40)
                pygame.draw.rect(layer, (30, 30, 30), billboard_rect, border_radius=6)
                layer.blit(logo, billboard_rect.topleft)
                font = pygame.font.Font(None, 18)
                text = font.render(sector_companies[company_idx]["name"], True, (255, 255, 255))
                layer.blit(text, (billboard_rect.centerx - text.get_width() // 2, billboard_rect.bottom + 2))
                company_idx += 1

            # Windows (flicker)
            for wx in range(10, width - 10, 20):
                for wy in range(40, height - 20, 30):
                    win_key = (x + wx, y_base - wy)
                    if win_key not in self.window_flicker_state:
                        self.window_flicker_state[win_key] = random.choice([True, False])
                    color = (255, 255, 180) if self.window_flicker_state[win_key] else (40, 40, 40)
                    pygame.draw.rect(layer, color, (x + wx, y_base - wy, 12, 18))

        # Animated drones (on top of all buildings)
        num_drones = 3
        if not self.drone_positions or len(self.drone_positions) != num_drones:
            self.drone_positions = [random.randint(0, self.screen_width * 2) for _ in range(num_drones)]
        drone_y = [random.randint(80, 200) for _ in range(num_drones)]
        drone_speed = [random.uniform(40, 80) for _ in range(num_drones)]
        drone_color = (180, 220, 255)
        drone_radius = 12
        for i in range(num_drones):
            self.drone_positions[i] = (self.drone_positions[i] + drone_speed[i] * 0.05) % (self.screen_width * 2)
            pygame.draw.circle(layer, drone_color, (int(self.drone_positions[i]), drone_y[i]), drone_radius)
            pygame.draw.circle(layer, (255, 0, 0), (int(self.drone_positions[i]) - 6, drone_y[i] + 4), 3)
            pygame.draw.circle(layer, (0, 255, 0), (int(self.drone_positions[i]) + 6, drone_y[i] + 4), 3)
            pygame.draw.line(layer, (100, 100, 100), (int(self.drone_positions[i]) - 10, drone_y[i] - 8), (int(self.drone_positions[i]) + 10, drone_y[i] - 8), 2)

        return {"surface": layer, "speed": 0.3, "offset": 0}

    def create_foreground_layer(self, sector_key):
        layer = pygame.Surface((self.screen_width * 2, self.screen_height), pygame.SRCALPHA)
        if sector_key == "SILICON_VALLEY":
            # Drones flying in foreground
            for i in range(2):
                x = random.randint(0, self.screen_width * 2)
                y = random.randint(self.screen_height-220, self.screen_height-180)
                pygame.draw.circle(layer, (180, 220, 255), (x, y), 18)
        elif sector_key == "TECH":
            # Rolling robots
            for i in range(2):
                x = random.randint(0, self.screen_width * 2)
                y = self.screen_height - 60
                pygame.draw.rect(layer, (100, 100, 120), (x, y, 40, 30), border_radius=8)
                pygame.draw.circle(layer, (0, 255, 0), (x+10, y+30), 8)
                pygame.draw.circle(layer, (0, 255, 0), (x+30, y+30), 8)
        elif sector_key == "ACADEMIA":
            # Books and caps
            for i in range(3):
                x = random.randint(0, self.screen_width * 2)
                y = self.screen_height - random.randint(80, 120)
                pygame.draw.rect(layer, (200, 180, 140), (x, y, 30, 10))
                pygame.draw.polygon(layer, (0, 0, 0), [(x, y), (x+30, y), (x+15, y-10)])
        elif sector_key == "CREATIVE":
            # Paint splashes
            for i in range(5):
                x = random.randint(0, self.screen_width * 2)
                y = self.screen_height - random.randint(60, 100)
                color = (random.randint(180, 255), random.randint(100, 255), random.randint(180, 255), 180)
                pygame.draw.ellipse(layer, color, (x, y, 30, 18))
        elif sector_key == "RETAIL":
            # Shopping carts
            for i in range(2):
                x = random.randint(0, self.screen_width * 2)
                y = self.screen_height - 50
                pygame.draw.rect(layer, (180, 180, 180), (x, y, 40, 20), border_radius=6)
                pygame.draw.circle(layer, (80, 80, 80), (x+10, y+20), 6)
                pygame.draw.circle(layer, (80, 80, 80), (x+30, y+20), 6)
        return {"surface": layer, "speed": 0.35, "offset": 0}

    def create_placeholder_layers(self, sector):
        self.layers = []
        sector_key = str(sector).upper()

        # 1. Sky (sector-specific gradient)
        sky_gradients = {
            "SILICON_VALLEY": [(80, 180, 255), (220, 255, 255)],
            "TECH": [(40, 60, 100), (120, 180, 220)],
            "ACADEMIA": [(255, 240, 200), (200, 180, 140)],
            "CREATIVE": [(255, 200, 220), (255, 255, 180)],
            "RETAIL": [(255, 255, 255), (255, 220, 180)],
        }
        top_color, bottom_color = sky_gradients.get(sector_key, [(30, 40, 80), (120, 180, 255)])
        layer0 = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        for y in range(self.screen_height):
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * (y / self.screen_height))
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * (y / self.screen_height))
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * (y / self.screen_height))
            pygame.draw.line(layer0, (r, g, b), (0, y), (self.screen_width, y))
        self.layers.append({"surface": layer0, "speed": 0.0, "offset": 0})

        # 2. Skyline (sector-specific)
        self.layers.append(self.create_skyline_layer(sector_key))

        # 3. Clouds (sector-specific)
        self.layers.append(self.create_cloud_layer(sector_key))

        # 4. Buildings (sector-specific)
        self.layers.append(self.create_building_layer(sector_key))

        # 5. Foreground (optional, sector-specific)
        self.layers.append(self.create_foreground_layer(sector_key))
        
    def update(self, delta_time, speed):
        for layer in self.layers:
            layer["offset"] = (layer["offset"] + speed * layer["speed"] * delta_time) % layer["surface"].get_width()
        self.billboard_offset = (self.billboard_offset + int(120 * delta_time)) % 400
        for key in self.window_flicker_state:
            if random.random() < 0.02:
                self.window_flicker_state[key] = not self.window_flicker_state[key]
            
    def draw(self, surface):
        for layer in self.layers:
            offset = int(layer["offset"])
            surface.blit(layer["surface"], (-offset, 0))
            surface.blit(layer["surface"], (layer["surface"].get_width() - offset, 0))
            
    def change_sector(self, sector):
        # Change clouds and buildings for new sector
        for i, layer in enumerate(self.layers):
            if layer["speed"] == 0.15:
                self.layers[i] = self.create_cloud_layer(sector)
            elif layer["speed"] == 0.3:
                self.layers[i] = self.create_building_layer(sector)

class ParticleSystem:
    def __init__(self):
        """Initialize particle system"""
        self.particles = []
        
    def add_stress_particles(self, x, y, count=10):
        """Add stress particles at position"""
        for _ in range(count):
            particle = {
                "x": x + random.randint(-20, 20),
                "y": y + random.randint(-20, 20),
                "vx": random.uniform(-50, 50),
                "vy": random.uniform(-100, -50),
                "size": random.randint(3, 8),
                "color": (255, 0, 0),
                "life": random.uniform(0.5, 1.5),
                "type": "stress"
            }
            self.particles.append(particle)
            
    def add_money_particles(self, x, y, count=15):
        """Add money particles at position"""
        for _ in range(count):
            particle = {
                "x": x + random.randint(-20, 20),
                "y": y + random.randint(-20, 20),
                "vx": random.uniform(-80, 80),
                "vy": random.uniform(-150, -50),
                "size": random.randint(5, 10),
                "color": (0, 200, 0),
                "life": random.uniform(0.3, 0.8),  # Short life for money
                "type": "money"
            }
            self.particles.append(particle)
            
    def add_diploma_particles(self, x, y, count=20):
        """Add diploma confetti particles"""
        for _ in range(count):
            particle = {
                "x": x + random.randint(-30, 30),
                "y": y + random.randint(-30, 30),
                "vx": random.uniform(-100, 100),
                "vy": random.uniform(-200, -100),
                "size": random.randint(5, 12),
                "color": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                "life": random.uniform(1.0, 3.0),
                "type": "diploma"
            }
            self.particles.append(particle)
            
    def add_anxiety_sparks(self, x, y, count=8):
        """Add anxiety spark particles around player"""
        for _ in range(count):
            angle = random.uniform(0, 6.28)  # 0 to 2π
            distance = random.uniform(20, 40)
            particle = {
                "x": x + distance * math.cos(angle),
                "y": y + distance * math.sin(angle),
                "vx": random.uniform(-20, 20),
                "vy": random.uniform(-20, 20),
                "size": random.randint(2, 5),
                "color": (255, 255, 0),  # Yellow sparks
                "life": random.uniform(0.2, 0.5),
                "type": "anxiety"
            }
            self.particles.append(particle)
            
    def update(self, delta_time):
        """Update all particles"""
        # Update existing particles
        for particle in self.particles[:]:
            # Update position
            particle["x"] += particle["vx"] * delta_time
            particle["y"] += particle["vy"] * delta_time
            
            # Apply gravity to some particle types
            if particle["type"] in ["money", "diploma"]:
                particle["vy"] += 200 * delta_time  # Gravity
                
            # Update life
            particle["life"] -= delta_time
            
            # Remove dead particles
            if particle["life"] <= 0:
                self.particles.remove(particle)
                
    def draw(self, surface):
        """Draw all particles"""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha = min(255, int(255 * (particle["life"] / 1.0)))
            
            if particle["type"] == "money":
                # Draw dollar sign
                font = pygame.font.Font(None, particle["size"] * 2)
                text = font.render("$", True, particle["color"])
                text.set_alpha(alpha)
                surface.blit(text, (particle["x"], particle["y"]))
            elif particle["type"] == "diploma":
                # Draw small rectangle for diploma
                rect = pygame.Surface((particle["size"], particle["size"] * 1.5))
                rect.fill(particle["color"])
                rect.set_alpha(alpha)
                surface.blit(rect, (particle["x"], particle["y"]))
            else:
                # Draw circle for other particle types
                particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    particle_surface, 
                    particle["color"] + (alpha,), 
                    (particle["size"], particle["size"]), 
                    particle["size"]
                )
                surface.blit(particle_surface, (particle["x"] - particle["size"], particle["y"] - particle["size"]))

def sector_to_str(sector):
    return sector.name if hasattr(sector, "name") else str(sector)

if __name__ == "__main__":
    # Test the visual elements
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Job Rush 2025 - Visual Test")
    clock = pygame.time.Clock()
    
    sprite_manager = SpriteManager()
    background = ParallaxBackground(1280, 720, "SILICON_VALLEY")
    particles = ParticleSystem()
    
    # Initialize layer offsets
    for layer in background.layers:
        layer["offset"] = 0
    
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Test particles on click
                x, y = pygame.mouse.get_pos()
                particles.add_stress_particles(x, y)
                particles.add_money_particles(x - 100, y)
                particles.add_diploma_particles(x + 100, y)
                particles.add_anxiety_sparks(x, y - 100)
                
        # Update background
        background.update(delta_time, 200)
        
        # Update particles
        particles.update(delta_time)
        
        # Draw everything
        screen.fill((0, 0, 0))
        background.draw(screen)
        
        # Draw some sprites for testing
        screen.blit(sprite_manager.get_sprite("player"), (100, 100))
        screen.blit(sprite_manager.get_sprite("ats_laser"), (200, 100))
        screen.blit(sprite_manager.get_sprite("skill_gap"), (350, 100))
        screen.blit(sprite_manager.get_sprite("experience_wall"), (450, 100))
        screen.blit(sprite_manager.get_sprite("burnout_cloud"), (550, 100))
        screen.blit(sprite_manager.get_sprite("recruiter_bot"), (650, 100))
        
        # Draw power-ups
        screen.blit(sprite_manager.get_sprite("nepotism_pass"), (100, 200))
        screen.blit(sprite_manager.get_sprite("linkedin_premium"), (150, 200))
        screen.blit(sprite_manager.get_sprite("mentorship_shield"), (200, 200))
        screen.blit(sprite_manager.get_sprite("bootcamp_speed"), (250, 200))
        
        # Draw UI elements
        for i in range(5):
            screen.blit(sprite_manager.get_sprite("coffee_cup"), (100 + i * 25, 250))
            
        # Draw particles
        particles.draw(screen)
        
        if self.flash_timer > 0:
            self.flash_timer -= delta_time
        if self.shake_timer > 0:
            self.shake_timer -= delta_time
            self.shake_offset = (random.randint(-6, 6), random.randint(-6, 6))
        else:
            self.shake_offset = (0, 0)
        
        pygame.display.flip()
        
    pygame.quit()
