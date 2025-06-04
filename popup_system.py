#!/usr/bin/env python3
import pygame
import random
import json
import os
from corporate_jargon import CorporateJargonGenerator

class PopupSystem:
    def __init__(self, screen_width, screen_height):
        """Initialize popup system for job postings and rejection letters"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Popup state
        self.active_popup = None
        self.popup_timer = 0
        self.popup_duration = 5.0  # Default duration in seconds
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (50, 50, 50)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Load jargon generator
        self.jargon_generator = CorporateJargonGenerator()
        
        # Popup templates
        self.job_posting_templates = [
            {
                "title": "Entry-level Developer",
                "description": "Looking for a rockstar ninja 10x developer with entrepreneurial spirit!",
                "requirements": [
                    "15 years React experience",
                    "PhD in Computer Science preferred",
                    "$30K salary (non-negotiable)",
                    "Must be willing to work weekends"
                ]
            },
            {
                "title": "Junior Marketing Associate",
                "description": "Be part of our fast-paced, dynamic team of thought leaders!",
                "requirements": [
                    "8+ years experience in digital marketing",
                    "MBA required, PhD preferred",
                    "Unpaid position with exposure",
                    "Must have own laptop"
                ]
            },
            {
                "title": "Administrative Assistant",
                "description": "Support our C-suite executives in a high-growth startup!",
                "requirements": [
                    "Master's degree minimum",
                    "Proficient in 12 software platforms",
                    "Willing to work 60+ hours/week",
                    "$15/hour (no benefits)"
                ]
            }
        ]
        
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
        
        self.game_ref = None  # Will be set by Game after creation
        self.sound_system = None
        
    def set_sound_system(self, sound_system):
        self.sound_system = sound_system
        
    def show_job_posting(self, duration=5.0):
        """Show a random job posting popup"""
        # Either use a template or generate a new one
        if random.random() < 0.5:
            job_template = random.choice(self.job_posting_templates)
            job_posting = job_template.copy()
        else:
            job_posting = self.jargon_generator.generate_job_posting()
            
        self.active_popup = {
            "type": "job_posting",
            "content": job_posting
        }
        self.popup_timer = 0
        self.popup_duration = duration
        
        if self.sound_system:
            self.sound_system.play_sound("job_posting")
        
    def show_rejection_letter(self, duration=5.0):
        """Show a random rejection letter popup"""
        rejection_text = random.choice(self.rejection_templates)
        
        self.active_popup = {
            "type": "rejection",
            "content": rejection_text
        }
        self.popup_timer = 0
        self.popup_duration = duration
        
        if self.sound_system:
            self.sound_system.play_sound("rejection_letter")
        
    def show_sector_transition(self, from_sector, to_sector, duration=3.0):
        """Show sector transition popup"""
        transition_texts = {
            "TECH→ACADEMIA": "Leaving silicon valley delusions... Entering ivory tower fantasies...",
            "ACADEMIA→CREATIVE": "Abandoning research stipends... Embracing starvation wages...",
            "CREATIVE→RETAIL": "Trading artistic freedom... For customer service nightmares...",
            "RETAIL→TECH": "Escaping minimum wage... For maximum burnout..."
        }
        
        transition_key = f"{from_sector}→{to_sector}"
        if transition_key in transition_texts:
            transition_text = transition_texts[transition_key]
        else:
            transition_text = f"Transitioning from {from_sector} to {to_sector}..."
            
        self.active_popup = {
            "type": "sector_transition",
            "content": {
                "from": from_sector,
                "to": to_sector,
                "text": transition_text
            }
        }
        self.popup_timer = 0
        self.popup_duration = duration
        
        if self.sound_system:
            self.sound_system.play_sound("sector_transition")
        
    def show_game_over(self, score, sector, duration=10.0):
        """Show game over popup with rejection letter generator"""
        self.active_popup = {
            "type": "game_over",
            "content": {
                "score": score,
                "sector": sector,
                "rejection": random.choice(self.rejection_templates)
            }
        }
        self.popup_timer = 0
        self.popup_duration = duration
        
        if self.sound_system:
            self.sound_system.play_sound("game_over")
        
    def update(self, delta_time):
        """Update popup timer"""
        if self.active_popup:
            self.popup_timer += delta_time
            if self.popup_timer >= self.popup_duration:
                self.active_popup = None
                
    def draw(self, surface):
        """Draw active popup if any"""
        if not self.active_popup:
            return
            
        # Draw popup background with semi-transparency
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        surface.blit(overlay, (0, 0))
        
        if self.active_popup["type"] == "job_posting":
            self.draw_job_posting(surface)
        elif self.active_popup["type"] == "rejection":
            self.draw_rejection_letter(surface)
        elif self.active_popup["type"] == "sector_transition":
            self.draw_sector_transition(surface)
        elif self.active_popup["type"] == "game_over":
            self.draw_game_over(surface)
            
    def draw_job_posting(self, surface):
        """Draw job posting popup"""
        job = self.active_popup["content"]
        
        # Draw popup box
        popup_width = 500
        popup_height = 300
        popup_x = self.screen_width // 2 - popup_width // 2
        popup_y = self.screen_height // 2 - popup_height // 2
        
        pygame.draw.rect(surface, self.GRAY, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(surface, self.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Draw header
        header_rect = pygame.Rect(popup_x, popup_y, popup_width, 40)
        pygame.draw.rect(surface, self.BLUE, header_rect)
        
        header_text = self.font_large.render("NEW JOB OPPORTUNITY!", True, self.WHITE)
        surface.blit(header_text, (popup_x + 10, popup_y + 10))
        
        # Draw job title
        title_text = self.font_medium.render(job["title"], True, self.WHITE)
        surface.blit(title_text, (popup_x + 10, popup_y + 50))
        
        # Draw description
        desc_text = self.font_small.render(job["description"], True, self.WHITE)
        surface.blit(desc_text, (popup_x + 10, popup_y + 80))
        
        # Draw requirements
        req_y = popup_y + 120
        req_header = self.font_medium.render("Requirements:", True, self.RED)
        surface.blit(req_header, (popup_x + 10, req_y))
        req_y += 30
        
        for req in job["requirements"]:
            req_text = self.font_small.render(f"• {req}", True, self.WHITE)
            surface.blit(req_text, (popup_x + 20, req_y))
            req_y += 25
            
        # Draw close button
        close_text = self.font_small.render("Click anywhere to close", True, self.WHITE)
        surface.blit(close_text, (popup_x + popup_width - close_text.get_width() - 10, popup_y + popup_height - 30))
        
    def draw_rejection_letter(self, surface):
        """Draw rejection letter popup"""
        rejection_text = self.active_popup["content"]
        
        # Draw popup box
        popup_width = 450
        popup_height = 200
        popup_x = self.screen_width // 2 - popup_width // 2
        popup_y = self.screen_height // 2 - popup_height // 2
        
        pygame.draw.rect(surface, self.GRAY, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(surface, self.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Draw header
        header_rect = pygame.Rect(popup_x, popup_y, popup_width, 40)
        pygame.draw.rect(surface, self.RED, header_rect)
        
        header_text = self.font_large.render("APPLICATION STATUS UPDATE", True, self.WHITE)
        surface.blit(header_text, (popup_x + 10, popup_y + 10))
        
        # Draw rejection text (word wrapped)
        words = rejection_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_width = self.font_medium.size(test_line)[0]
            
            if text_width < popup_width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
                
        if current_line:
            lines.append(current_line)
            
        text_y = popup_y + 60
        for line in lines:
            line_text = self.font_medium.render(line, True, self.WHITE)
            surface.blit(line_text, (popup_x + 20, text_y))
            text_y += 30
            
        # Draw close button
        close_text = self.font_small.render("Click anywhere to close", True, self.WHITE)
        surface.blit(close_text, (popup_x + popup_width - close_text.get_width() - 10, popup_y + popup_height - 30))
        
    def draw_sector_transition(self, surface):
        """Draw sector transition popup"""
        transition = self.active_popup["content"]
        
        # Draw popup box
        popup_width = 600
        popup_height = 150
        popup_x = self.screen_width // 2 - popup_width // 2
        popup_y = self.screen_height // 2 - popup_height // 2
        
        pygame.draw.rect(surface, self.GRAY, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(surface, self.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Draw header
        header_text = self.font_large.render(f"SECTOR TRANSITION: {transition['from']} → {transition['to']}", True, self.WHITE)
        surface.blit(header_text, (popup_x + (popup_width - header_text.get_width()) // 2, popup_y + 20))
        
        # Draw transition text
        trans_text = self.font_medium.render(transition["text"], True, self.RED)
        surface.blit(trans_text, (popup_x + (popup_width - trans_text.get_width()) // 2, popup_y + 70))
        
        # Draw progress bar
        progress = min(1.0, self.popup_timer / self.popup_duration)
        bar_width = 500
        bar_height = 20
        bar_x = popup_x + (popup_width - bar_width) // 2
        bar_y = popup_y + 110
        
        pygame.draw.rect(surface, self.WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        pygame.draw.rect(surface, self.BLUE, (bar_x, bar_y, int(bar_width * progress), bar_height))
        
    def draw_game_over(self, surface):
        """Draw game over popup with rejection letter generator"""
        game_over = self.active_popup["content"]
        
        # Draw popup box
        popup_width = 600
        popup_height = 400
        popup_x = self.screen_width // 2 - popup_width // 2
        popup_y = self.screen_height // 2 - popup_height // 2
        
        pygame.draw.rect(surface, self.GRAY, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(surface, self.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Draw header
        header_rect = pygame.Rect(popup_x, popup_y, popup_width, 50)
        pygame.draw.rect(surface, self.RED, header_rect)
        
        header_text = self.font_large.render("REJECTION LETTER GENERATOR", True, self.WHITE)
        surface.blit(header_text, (popup_x + (popup_width - header_text.get_width()) // 2, popup_y + 15))
        
        # Draw score
        score_text = self.font_medium.render(f"Final Score: {int(game_over['score'])} Synergy Points", True, self.WHITE)
        surface.blit(score_text, (popup_x + 20, popup_y + 70))
        
        # Draw sector
        sector_text = self.font_medium.render(f"Final Sector: {game_over['sector']}", True, self.WHITE)
        surface.blit(sector_text, (popup_x + 20, popup_y + 100))
        
        # Draw divider
        pygame.draw.line(surface, self.WHITE, (popup_x + 20, popup_y + 130), (popup_x + popup_width - 20, popup_y + 130), 2)
        
        # Draw rejection letter header
        letter_header = self.font_medium.render("Your Official Rejection Letter:", True, self.RED)
        surface.blit(letter_header, (popup_x + 20, popup_y + 150))
        
        # Draw AI review note
        ai_text = self.font_small.render("Your application was reviewed by our AI (a magic 8-ball)", True, self.WHITE)
        surface.blit(ai_text, (popup_x + 20, popup_y + 180))
        
        # Draw rejection text (word wrapped)
        words = game_over["rejection"].split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_width = self.font_medium.size(test_line)[0]
            
            if text_width < popup_width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
                
        if current_line:
            lines.append(current_line)
            
        text_y = popup_y + 210
        for line in lines:
            line_text = self.font_medium.render(line, True, self.WHITE)
            surface.blit(line_text, (popup_x + 20, text_y))
            text_y += 30
            
        # Draw social share button
        share_box = pygame.Rect(popup_x + 150, popup_y + 320, 300, 40)
        pygame.draw.rect(surface, self.BLUE, share_box)
        pygame.draw.rect(surface, self.WHITE, share_box, 2)
        
        share_text = self.font_medium.render("Share Your Failure", True, self.WHITE)
        surface.blit(share_text, (share_box.x + (share_box.width - share_text.get_width()) // 2, share_box.y + 10))
        
        # Draw hashtags
        hashtag_text = self.font_small.render("#JobRushSurvival #AmazonQCLI", True, self.WHITE)
        surface.blit(hashtag_text, (popup_x + (popup_width - hashtag_text.get_width()) // 2, popup_y + 370))
        
    def handle_click(self, pos):
        """Handle mouse click on popup"""
        if not self.active_popup:
            return False
            
        # For job postings and rejection letters, any click closes them
        if self.active_popup["type"] in ["job_posting", "rejection"]:
            if self.sound_system:
                self.sound_system.play_sound("button_click")
            self.active_popup = None
            return True
            
        # For game over popup, check if share button was clicked
        if self.active_popup["type"] == "game_over":
            popup_width = 600
            popup_height = 400
            popup_x = self.screen_width // 2 - popup_width // 2
            popup_y = self.screen_height // 2 - popup_height // 2
            
            share_box = pygame.Rect(popup_x + 150, popup_y + 320, 300, 40)
            if share_box.collidepoint(pos):
                # In a real game, this would share to social media
                print("Sharing to social media...")
                return True
                
        return False

if __name__ == "__main__":
    # Test the popup system
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Job Rush 2025 - Popup Test")
    clock = pygame.time.Clock()
    
    popup_system = PopupSystem(1280, 720)
    
    # Show initial popup
    popup_system.show_job_posting()
    
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    popup_system.show_job_posting()
                elif event.key == pygame.K_2:
                    popup_system.show_rejection_letter()
                elif event.key == pygame.K_3:
                    popup_system.show_sector_transition("TECH", "ACADEMIA")
                elif event.key == pygame.K_4:
                    popup_system.show_game_over(1500, "TECH")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                popup_system.handle_click(event.pos)
                
        # Update popup
        popup_system.update(delta_time)
        
        # Draw everything
        screen.fill((0, 0, 0))
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Press 1: Show Job Posting",
            "Press 2: Show Rejection Letter",
            "Press 3: Show Sector Transition",
            "Press 4: Show Game Over",
            "Click: Interact with popups"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, (255, 255, 255))
            screen.blit(text, (20, 20 + i * 30))
            
        # Draw popup
        popup_system.draw(screen)
        
        pygame.display.flip()
        
    pygame.quit()
