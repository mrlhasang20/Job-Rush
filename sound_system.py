#!/usr/bin/env python3
import pygame
import os
import sys
from resource_path import resource_path

class SoundSystem:
    def __init__(self, audio_available=True):
        print(f"Pygame version: {pygame.version.ver}")
        self.audio_available = audio_available
        self.sfx = {}
        self.bgm = {}
        self.current_music = None
        
        # Initialize pygame mixer with specific settings
        try:
            pygame.mixer.quit()  # First quit any existing mixer
            pygame.mixer.init(44100, -16, 2, 2048)
            print(f"Pygame audio driver: {pygame.mixer.get_init()}")
        except pygame.error as e:
            print(f"Failed to initialize pygame mixer: {e}")
            self.audio_available = False
            return

        # Test audio initialization with a simple sound
        test_sound = "button_click.wav"
        test_path = resource_path(os.path.join("assets", "sounds", test_sound))
        print(f"Testing sound path: {test_path}")
        
        try:
            if os.path.exists(test_path):
                print(f"Test sound file exists at: {test_path}")
                test_sound_obj = pygame.mixer.Sound(test_path)
                test_sound_obj.play()
                pygame.time.wait(100)  # Wait a bit to ensure sound plays
                test_sound_obj.stop()
                print("Audio initialization successful")
                self.audio_available = True
            else:
                print(f"Warning: Test sound file not found at {test_path}")
                # Try alternative path
                alt_test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds", test_sound)
                if os.path.exists(alt_test_path):
                    print(f"Found sound at alternative path: {alt_test_path}")
                    test_sound_obj = pygame.mixer.Sound(alt_test_path)
                    test_sound_obj.play()
                    pygame.time.wait(100)
                    test_sound_obj.stop()
                    print("Audio initialization successful with alternative path")
                    self.audio_available = True
                else:
                    print("Game will run without sound.")
                    self.audio_available = False
                    return
        except Exception as e:
            print(f"Warning: Audio initialization failed: {e}")
            self.audio_available = False
            return

        if self.audio_available:
            self.load_sounds()
            self.play_background_music()

    def load_sounds(self):
        if not self.audio_available:
            return
            
        try:
            sound_files = {
                "jump": "jump.wav",
                "slide": "slide.wav",
                "lane_change": "lane_change.wav",
                "skill_gap": "skill_gap.wav",
                "ats_laser": "ats_laser.wav",
                "experience_wall": "experience_wall.wav",
                "burnout_cloud": "burnout_cloud.wav",
                "recruiter_bot": "recruiter_bot.wav",
                "nepotism_pass": "nepotism_pass.wav",
                "linkedin_premium": "linkedin_premium.wav",
                "mentorship_shield": "mentorship_shield.wav",
                "bootcamp_speed": "bootcamp_speed.wav",
                "sector_transition": "sector_transition.wav",
                "button_click": "button_click.wav",
                "job_posting": "job_posting.wav",
                "rejection_letter": "rejection_letter.wav",
                "game_over": "game_over.wav",
                "heave": "heave.wav"
            }

            for sound_name, filename in sound_files.items():
                try:
                    file_path = resource_path(os.path.join("assets", "sounds", filename))
                    print(f"Loading sound {sound_name} from: {file_path}")
                    if os.path.exists(file_path):
                        self.sfx[sound_name] = pygame.mixer.Sound(file_path)
                        self.sfx[sound_name].set_volume(0.2)
                        print(f"Successfully loaded sound: {sound_name}")
                    else:
                        print(f"Warning: Sound file not found: {file_path}")
                except Exception as e:
                    print(f"Warning: Could not load sound {sound_name}: {e}")

            # Background music files
            bgm_path = resource_path(os.path.join("assets", "sounds", "background.wav"))
            print(f"Loading background music from: {bgm_path}")
            
            if os.path.exists(bgm_path):
                self.bgm = {
                    "background": bgm_path,
                    "SILICON_VALLEY": bgm_path
                }
                print("Background music paths loaded successfully")
            else:
                print(f"Warning: Background music file not found: {bgm_path}")

        except Exception as e:
            print(f"Warning: Error in sound system initialization: {e}")
            self.audio_available = False

    def play_sound(self, sound_name):
        if not self.audio_available:
            print("Audio not available")
            return
        try:
            if sound_name in self.sfx:
                print(f"Playing sound: {sound_name}")
                # Stop any previous instance of this sound
                self.sfx[sound_name].stop()
                self.sfx[sound_name].play()
            else:
                print(f"Sound not found: {sound_name}")
        except pygame.error as e:
            print(f"Error playing sound {sound_name}: {e}")
        except Exception as e:
            print(f"Unexpected error playing sound {sound_name}: {e}")

    def play_bgm(self, sector):
        """Play background music based on the current sector"""
        if not self.audio_available:
            print("Audio not available for BGM")
            return
        try:
            print(f"Attempting to play BGM for sector: {sector}")
            # If we're in Silicon Valley sector, play Silicon Valley music
            if sector == "SILICON_VALLEY":
                self.play_silicon_valley_music()
            else:
                self.play_background_music()
        except pygame.error as e:
            print(f"Error playing BGM: {e}")

    def play_background_music(self):
        """Play the main background music"""
        if not self.audio_available:
            print("Audio not available for background music")
            return
        try:
            # Only change music if we're not already playing background music
            if self.current_music != "background":
                print("Loading background music")
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.bgm["background"])
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
                self.current_music = "background"
                print("Background music started successfully")
        except pygame.error as e:
            print(f"Error playing background music: {e}")
        except Exception as e:
            print(f"Unexpected error playing background music: {e}")

    def play_silicon_valley_music(self):
        """Play Silicon Valley background music"""
        if not self.audio_available:
            print("Audio not available for Silicon Valley music")
            return
        try:
            # Only change music if we're not already playing Silicon Valley music
            if self.current_music != "SILICON_VALLEY":
                print("Loading Silicon Valley music")
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.bgm["SILICON_VALLEY"])
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
                self.current_music = "SILICON_VALLEY"
                print("Silicon Valley music started successfully")
        except pygame.error as e:
            print(f"Error playing Silicon Valley music: {e}")
            # If Silicon Valley music fails, fall back to background music
            self.play_background_music()

    def update(self):
        """Update sound system - check if music needs to be restarted"""
        if not self.audio_available:
            return
            
        try:
            # Check if music has stopped
            if not pygame.mixer.music.get_busy():
                # Restart the current music
                if self.current_music == "SILICON_VALLEY":
                    self.play_silicon_valley_music()
                else:
                    self.play_background_music()
        except pygame.error as e:
            print(f"Error in sound system update: {e}")
