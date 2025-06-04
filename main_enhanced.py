#!/usr/bin/env python3
import pygame
import sys
import random
import json
import time
import math
from enum import Enum
import os

# Import our enhanced game
from game_enhanced import Game
from outro_sequence import OutroSequence

# Initialize pygame
pygame.init()

# Print pygame version and audio driver info
print(f"Pygame version: {pygame.version.ver}")
print(f"Pygame audio driver: {pygame.mixer.get_init()}")

# Try to initialize audio with different settings
audio_available = False
try:
    # Try different audio settings
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    
    # Test if audio is working by loading a sound
    test_sound = pygame.mixer.Sound("assets/sounds/button_click.wav")
    test_sound.play()
    time.sleep(0.1)  # Wait a bit to hear the sound
    audio_available = True
    print("Audio system initialized successfully!")
except pygame.error as e:
    print(f"Warning: Could not initialize audio: {e}")
    print("Game will run without sound.")
    audio_available = False
except Exception as e:
    print(f"Warning: Unexpected error during audio initialization: {e}")
    print("Game will run without sound.")
    audio_available = False

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Job Rush 2025 @ Lhasang T Lama")
clock = pygame.time.Clock()

def main():
    # Create and run the game
    game = Game(screen, clock, audio_available)
    result = game.run()

    if result == "quit":
        outro = OutroSequence(screen, clock)
        outro.run()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
