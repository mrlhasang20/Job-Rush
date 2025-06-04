#!/usr/bin/env python3
import pygame
import os

class SoundSystem:
    def __init__(self, audio_available=True):
        self.audio_available = audio_available
        self.sfx = {}
        self.bgm = {}
        self.current_music = None
        if self.audio_available:
            self.load_sounds()
            # Start playing background music immediately
            self.play_background_music()

    def load_sounds(self):
        if not self.audio_available:
            return
            
        try:
            sound_dir = "assets/sounds"
            
            # Load sound effects with error handling for each sound
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
                    file_path = os.path.join(sound_dir, filename)
                    if os.path.exists(file_path):
                        self.sfx[sound_name] = pygame.mixer.Sound(file_path)
                        self.sfx[sound_name].set_volume(0.2)  # Lower volume for sound effects
                except pygame.error as e:
                    print(f"Warning: Could not load sound {sound_name}: {e}")

            # Background music files
            self.bgm = {
                "background": os.path.join(sound_dir, "background.wav"),
                "SILICON_VALLEY": os.path.join(sound_dir, "background.wav")
            }

        except Exception as e:
            print(f"Warning: Error in sound system initialization: {e}")
            self.audio_available = False

    def play_sound(self, sound_name):
        if not self.audio_available:
            return
        try:
            if sound_name in self.sfx:
                # Stop any previous instance of this sound
                self.sfx[sound_name].stop()
                self.sfx[sound_name].play()
        except pygame.error:
            pass

    def play_bgm(self, sector):
        """Play background music based on the current sector"""
        if not self.audio_available:
            return
        try:
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
            return
        try:
            # Only change music if we're not already playing background music
            if self.current_music != "background":
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.bgm["background"])
                pygame.mixer.music.set_volume(0.1)  # Lower volume for background music
                pygame.mixer.music.play(-1)  # -1 means loop forever
                self.current_music = "background"
        except pygame.error as e:
            print(f"Error playing background music: {e}")

    def play_silicon_valley_music(self):
        """Play Silicon Valley background music"""
        if not self.audio_available:
            return
        try:
            # Only change music if we're not already playing Silicon Valley music
            if self.current_music != "SILICON_VALLEY":
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.bgm["SILICON_VALLEY"])
                pygame.mixer.music.set_volume(0.1)  # Lower volume for background music
                pygame.mixer.music.play(-1)  # -1 means loop forever
                self.current_music = "SILICON_VALLEY"
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
        except pygame.error:
            pass
