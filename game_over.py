#!/usr/bin/env python3
import pygame
import sys
import random
import pyperclip
from outro_sequence import OutroSequence

class GameOverScreen:
    def __init__(self, screen, clock, score, sector, player_name="Graduate"):
        """Initialize game over screen with player stats"""
        self.screen = screen
        self.clock = clock
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.score = score
        self.sector = sector
        self.player_name = player_name
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (50, 50, 50)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 255, 0)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Generate random stats
        self.years_experience = int(score / 100)
        self.buzzwords_learned = int(score / 50)
        self.dreams_crushed = int(score / 75)
        self.coffee_consumed = round(score / 200, 1)
        
        # Rejection letter templates
        self.rejection_templates = [
            "Thank you for applying. We've decided to hire the CEO's nephew instead.",
            "After careful consideration, we've determined you're overqualified. Have you considered McDonald's?",
            "Your application was impressive, but we're looking for someone with more experience in being exploited.",
            "We've received your application and will keep your resume on file (in the trash).",
            "While your qualifications are excellent, we've decided to go with someone who will work for less money.",
            "Thank you for your interest. The position has been filled by someone who knows the hiring manager.",
            "We regret to inform you that we've decided to hire internally (the boss's son).",
            "Your application was reviewed by our AI (a magic 8-ball) and the answer was 'Ask again later'.",
            "We appreciate your time, but we're looking for someone with the exact same experience but somehow also more.",
            "After reviewing your application, we've decided you're too qualified to be paid this little."
        ]
        
        # Select a random rejection letter
        self.rejection_letter = random.choice(self.rejection_templates)
        
        # Button states
        self.restart_hover = False
        self.quit_hover = False
        self.share_hover = False
        
        # Mockery text
        # self.mockery_text = f"Congratulations! You survived {int(score / 100)} seconds in the job market. That's {int(score / 100) - 1} seconds longer than your last relationship with hope."
        
    def draw(self):
        # Fill background
        self.screen.fill(self.BLACK)

        # Card for content
        card_width = 700
        card_height = 520
        card_x = self.width // 2 - card_width // 2
        card_y = self.height // 2 - card_height // 2
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        pygame.draw.rect(self.screen, (36, 36, 36), card_rect, border_radius=18)
        pygame.draw.rect(self.screen, self.WHITE, card_rect, 2, border_radius=18)

        y = card_y + 30

        # GAME OVER
        game_over_text = self.font_large.render("GAME OVER", True, self.RED)
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, y))
        y += 60

        # Rejection Letter Generator
        rej_header = self.font_medium.render("REJECTION LETTER GENERATOR", True, self.WHITE)
        self.screen.blit(rej_header, (self.width // 2 - rej_header.get_width() // 2, y))
        y += 40

        # AI review note
        ai_text = self.font_small.render("Your application was reviewed by our AI (a magic 8-ball)", True, (120, 120, 120))
        self.screen.blit(ai_text, (self.width // 2 - ai_text.get_width() // 2, y))
        y += 30

        # Rejection letter (wrapped)
        self.draw_wrapped_text(self.rejection_letter, self.font_medium, self.WHITE, self.width // 2, y, max_width=card_width-60, center=True)
        y += 80

        # Stats card
        stats_card = pygame.Rect(card_x + 40, y, card_width - 80, 180)
        pygame.draw.rect(self.screen, (20, 20, 40), stats_card, border_radius=10)
        pygame.draw.rect(self.screen, self.BLUE, stats_card, 2, border_radius=10)

        stats_y = y + 10
        stats_header = self.font_medium.render("YOUR CAREER STATS:", True, self.BLUE)
        self.screen.blit(stats_header, (self.width // 2 - stats_header.get_width() // 2, stats_y))
        stats_y += 35

        stats = [
            f"Synergy Points: {int(self.score)}",
            f"Years of Experience Faked: {self.years_experience}",
            f"Buzzwords Learned: {self.buzzwords_learned}",
            f"Dreams Crushed: {self.dreams_crushed}",
            f"Coffee Consumed: {self.coffee_consumed} Liters"
        ]
        for stat in stats:
            stat_text = self.font_small.render(stat, True, self.WHITE)
            self.screen.blit(stat_text, (self.width // 2 - stat_text.get_width() // 2, stats_y))
            stats_y += 25

        # Buttons
        button_y = card_y + card_height - 80
        button_w, button_h = 180, 54
        spacing = 40
        self.restart_rect = pygame.Rect(self.width // 2 - button_w - spacing // 2, button_y, button_w, button_h)
        self.quit_rect = pygame.Rect(self.width // 2 + spacing // 2, button_y, button_w, button_h)
        self.share_rect = pygame.Rect(self.width // 2 - 90, button_y + 65, 180, 40)

        # Restart button
        pygame.draw.rect(self.screen, (0, 120, 255) if self.restart_hover else (40, 40, 80), self.restart_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.WHITE, self.restart_rect, 2, border_radius=12)
        restart_text = self.font_medium.render("Restart", True, self.WHITE)
        self.screen.blit(restart_text, (self.restart_rect.centerx - restart_text.get_width() // 2, self.restart_rect.centery - restart_text.get_height() // 2))

        # Quit button
        pygame.draw.rect(self.screen, (200, 40, 40) if self.quit_hover else (80, 40, 40), self.quit_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.WHITE, self.quit_rect, 2, border_radius=12)
        quit_text = self.font_medium.render("Quit", True, self.WHITE)
        self.screen.blit(quit_text, (self.quit_rect.centerx - quit_text.get_width() // 2, self.quit_rect.centery - quit_text.get_height() // 2))

        # Share Results button
        pygame.draw.rect(self.screen, (40, 180, 80) if self.share_hover else (40, 40, 80), self.share_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, self.share_rect, 2, border_radius=10)
        share_text = self.font_small.render("Share Results", True, self.WHITE)
        self.screen.blit(share_text, (self.share_rect.centerx - share_text.get_width() // 2, self.share_rect.centery - share_text.get_height() // 2))


        # Feedback for copied
        if getattr(self, "share_copied", False):
            copied_text = self.font_small.render("Copied!", True, (0, 255, 0))
            self.screen.blit(copied_text, (self.share_rect.centerx - copied_text.get_width() // 2, self.share_rect.bottom + 5))

        pygame.display.flip()
        
    def draw_wrapped_text(self, text, font, color, x, y, max_width=500, center=False):
        """Draw text wrapped to fit within max_width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_width = font.size(test_line)[0]
            
            if text_width < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
                
        if current_line:
            lines.append(current_line)
            
        for i, line in enumerate(lines):
            if center:
                line_surface = font.render(line, True, color)
                line_rect = line_surface.get_rect(center=(x, y + i * (font.get_height() + 5)))
                self.screen.blit(line_surface, line_rect)
            else:
                line_surface = font.render(line, True, color)
                self.screen.blit(line_surface, (x, y + i * (font.get_height() + 5)))
                
    def draw_buttons(self):
        """Draw restart and quit buttons"""
        # Restart button
        restart_color = self.GREEN if self.restart_hover else self.BLUE
        restart_rect = pygame.Rect(self.width // 2 - 150, 570, 140, 50)
        pygame.draw.rect(self.screen, restart_color, restart_rect)
        pygame.draw.rect(self.screen, self.WHITE, restart_rect, 2)
        
        restart_text = self.font_medium.render("Restart", True, self.WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        self.screen.blit(restart_text, restart_text_rect)
        
        # Quit button
        quit_color = self.RED if self.quit_hover else self.GRAY
        quit_rect = pygame.Rect(self.width // 2 + 10, 570, 140, 50)
        pygame.draw.rect(self.screen, quit_color, quit_rect)
        pygame.draw.rect(self.screen, self.WHITE, quit_rect, 2)
        
        quit_text = self.font_medium.render("Quit", True, self.WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        self.screen.blit(quit_text, quit_text_rect)
        
        # Share button
        share_color = self.BLUE if self.share_hover else self.GRAY
        share_rect = pygame.Rect(self.width // 2 - 70, 630, 140, 30)
        pygame.draw.rect(self.screen, share_color, share_rect)
        pygame.draw.rect(self.screen, self.WHITE, share_rect, 2)
        
        share_text = self.font_small.render("Share Results", True, self.WHITE)
        share_text_rect = share_text.get_rect(center=share_rect.center)
        self.screen.blit(share_text, share_text_rect)
        
    def get_share_message(self):
        seconds = int(self.score / 100)
        sector = self.sector if isinstance(self.sector, str) else getattr(self.sector, "name", str(self.sector))
        templates = [
            f"Survived {seconds}s in the 2025 job market sim. Final sector: {sector}. Rejected harder than my last situationship. Think you can out-fail me? #JobRushSurvival #GenZGrind #LateStageCapitalism",
            f"I lasted {seconds} seconds before capitalism chewed me up and spat me out in {sector}. HR ghosted me, but at least my coffee addiction is thriving. #HustleCulture #JobRushSurvival",
            f"Just got laid off in {sector} after {seconds}s. My resume is now a modern art piece. Can you beat my record? #UnemployedAndUnbothered #JobRushSurvival",
            f"Made it {seconds}s in the 2025 job market. Final sector: {sector}. My dreams: crushed. My spirit: still memeable. #Grindset #JobRushSurvival",
            f"POV: You, me, and {seconds}s of job market pain in {sector}. Swipe left on my career, but right on this game. #JobRushSurvival #CorporateL",
        ]
        return random.choice(templates)

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return "restart"
            if event.type == pygame.MOUSEMOTION:
                # Check button hover states
                restart_rect = pygame.Rect(self.width // 2 - 150, 570, 140, 50)
                quit_rect = pygame.Rect(self.width // 2 + 10, 570, 140, 50)
                share_rect = pygame.Rect(self.width // 2 - 70, 630, 140, 30)
                
                self.restart_hover = restart_rect.collidepoint(event.pos)
                self.quit_hover = quit_rect.collidepoint(event.pos)
                self.share_hover = share_rect.collidepoint(event.pos)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check button clicks
                restart_rect = pygame.Rect(self.width // 2 - 150, 570, 140, 50)
                quit_rect = pygame.Rect(self.width // 2 + 10, 570, 140, 50)
                share_rect = pygame.Rect(self.width // 2 - 70, 630, 140, 30)
                
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                elif quit_rect.collidepoint(event.pos):
                    return "quit"
                elif share_rect.collidepoint(event.pos):
                    # Copy to clipboard
                    try:
                        pyperclip.copy(self.get_social_share_text())
                        self.share_copied = True
                        self.share_copied_timer = pygame.time.get_ticks()
                    except Exception as e:
                        print("Clipboard error:", e)
        return None
        
    def run(self):
        """Run the game over screen until user makes a choice"""
        import pyperclip
        running = True
        self.share_copied = False
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Play outro before quitting
                    from outro_sequence import OutroSequence
                    outro = OutroSequence(self.screen, self.clock)
                    outro.run()
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    self.restart_hover = self.restart_rect.collidepoint(mx, my)
                    self.quit_hover = self.quit_rect.collidepoint(mx, my)
                    self.share_hover = self.share_rect.collidepoint(mx, my)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if self.restart_rect.collidepoint(mx, my):
                        return "restart"
                    elif self.quit_rect.collidepoint(mx, my):
                        from outro_sequence import OutroSequence
                        outro = OutroSequence(self.screen, self.clock)
                        outro.run()
                        pygame.quit()
                        exit()
                    elif self.share_rect.collidepoint(mx, my):
                        pyperclip.copy(self.get_share_message())
                        self.share_copied = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return "restart"
                    elif event.key == pygame.K_ESCAPE:
                        from outro_sequence import OutroSequence
                        outro = OutroSequence(self.screen, self.clock)
                        outro.run()
                        pygame.quit()
                        exit()
            self.clock.tick(60)
            
        return "quit"

if __name__ == "__main__":
    # Test the game over screen
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Job Rush 2025 - Game Over Test")
    clock = pygame.time.Clock()
    
    game_over = GameOverScreen(screen, clock, 1500, "TECH", "TestPlayer")
    result = game_over.run()
    
    print(f"Result: {result}")
    if result == "quit":
        outro = OutroSequence(screen, clock)
        outro.run()
        pygame.quit()
        sys.exit()

def outro_screen(screen, clock):
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)
    screen.fill((0, 0, 0))
    thank_you = font.render("Thanks for playing Job Rush 2025!", True, (255, 255, 255))
    share = small_font.render("Share your results and challenge your friends!", True, (255, 255, 0))
    screen.blit(thank_you, (screen.get_width() // 2 - thank_you.get_width() // 2, screen.get_height() // 2 - 40))
    screen.blit(share, (screen.get_width() // 2 - share.get_width() // 2, screen.get_height() // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(2500)
