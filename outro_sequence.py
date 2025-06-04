import pygame
import sys
import time
import textwrap

class OutroSequence:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GRAY = (50, 50, 50)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.state = 0
        self.alpha = 0
        self.fade_direction = 1
        self.state_timer = 0
        self.last_time = time.time()
        self.delta_time = 0

        self.outro_lines = [
            ("THANK YOU FOR PLAYING JOB RUSH 2025!", self.WHITE),
            ("Your resume has been shredded for your safety.", self.RED),
            ("Remember: Every rejection is just a new opportunity to question your life choices.", self.WHITE),
            ("Share your results and let your friends know they're not alone in the job market!", self.BLUE),
            ("May your inbox be ever full of interviews (and not just spam).", self.WHITE),
            ("See you in the next round of layoffs!", self.RED),
        ]

    def run(self):
        for text, color in self.outro_lines:
            self.state_timer = 0
            self.alpha = 0
            self.fade_direction = 1
            while self.alpha < 255:
                self.update()
                self.draw(text, color)
                pygame.display.flip()
                self.clock.tick(60)
            time.sleep(1.5)
            self.fade_direction = -1
            while self.alpha > 0:
                self.update()
                self.draw(text, color)
                pygame.display.flip()
                self.clock.tick(60)
        # Wait a moment before quitting
        time.sleep(1.0)

    def update(self):
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
        self.alpha += self.fade_direction * 255 * self.delta_time
        self.alpha = max(0, min(255, self.alpha))

    def draw(self, text, color):
        self.screen.fill((0, 0, 0))
        max_width = int(self.width * 0.85)
        lines = self.wrap_text(text, self.font_large, max_width)
        total_height = len(lines) * (self.font_large.get_height() + 10)
        y_start = self.height // 2 - total_height // 2

        for i, line in enumerate(lines):
            text_surface = self.font_large.render(line, True, color)
            text_surface.set_alpha(int(self.alpha))
            text_rect = text_surface.get_rect(center=(self.width // 2, y_start + i * (self.font_large.get_height() + 10)))
            self.screen.blit(text_surface, text_rect)

    def wrap_text(self, text, font, max_width):
        """Splits text into lines that fit within max_width."""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines
