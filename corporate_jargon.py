#!/usr/bin/env python3
import json
import random
import os

class CorporateJargonGenerator:
    def __init__(self):
        self.buzzwords = {
            "nouns": [
                "synergy", "paradigm", "leverage", "bandwidth", "deliverable",
                "stakeholder", "mindshare", "ecosystem", "pipeline", "roadmap",
                "strategy", "alignment", "engagement", "value-add", "KPI",
                "ROI", "actionable", "scalability", "innovation", "disruption"
            ],
            "verbs": [
                "leverage", "synergize", "optimize", "streamline", "ideate",
                "incentivize", "monetize", "strategize", "disrupt", "pivot",
                "onboard", "offboard", "deep-dive", "circle back", "touch base",
                "reach out", "drill down", "unpack", "align", "cascade"
            ],
            "adjectives": [
                "robust", "scalable", "agile", "lean", "cutting-edge",
                "best-in-class", "world-class", "next-generation", "innovative", "disruptive",
                "strategic", "mission-critical", "customer-centric", "data-driven", "results-oriented",
                "forward-thinking", "high-level", "low-hanging", "bleeding-edge", "game-changing"
            ],
            "phrases": [
                "think outside the box",
                "move the needle",
                "at the end of the day",
                "hit the ground running",
                "all hands on deck",
                "take it offline",
                "circle back",
                "put a pin in it",
                "boil the ocean",
                "drink from the firehose",
                "eat our own dog food",
                "open the kimono",
                "peel the onion",
                "push the envelope",
                "reinvent the wheel"
            ]
        }
        
        self.job_titles = [
            "Thought Leader",
            "Innovation Ninja",
            "Digital Overlord",
            "Chief Happiness Officer",
            "Growth Hacker",
            "Rockstar Developer",
            "Wizard of Light Bulb Moments",
            "Brand Evangelist",
            "Dream Alchemist",
            "Full Stack Magician",
            "Director of First Impressions",
            "Chief People Pleaser",
            "Sustainability Guru",
            "Paradigm Shifter",
            "Disruption Advocate"
        ]
        
        self.job_requirements = [
            "10+ years experience with 2-year-old technology",
            "Must be a team player who works independently",
            "Entry level position requiring 5+ years experience",
            "Competitive salary (well below market rate)",
            "Unlimited vacation (that you can never take)",
            "Fast-paced environment (understaffed)",
            "Work hard, play hard (80+ hour weeks)",
            "Flexible hours (always on call)",
            "Self-starter (no training provided)",
            "Wear multiple hats (do multiple jobs for one salary)",
            "Competitive benefits (standard benefits)",
            "Family atmosphere (unprofessional boundaries)",
            "Passionate about the mission (willing to work for less)",
            "Rockstar developer (unrealistic expectations)",
            "Must love dogs (CEO brings untrained pet to office)"
        ]
        
        # Ensure data directory exists
        os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
        
        # Save jargon to JSON file
        self.save_jargon()
        
    def save_jargon(self):
        """Save corporate jargon to JSON file"""
        jargon_data = {
            "buzzwords": self.buzzwords,
            "job_titles": self.job_titles,
            "job_requirements": self.job_requirements
        }
        
        with open(os.path.join(os.path.dirname(__file__), "data", "corporate_jargon.json"), "w") as f:
            json.dump(jargon_data, f, indent=4)
            
    def load_jargon(self):
        """Load corporate jargon from JSON file"""
        try:
            with open(os.path.join(os.path.dirname(__file__), "data", "corporate_jargon.json"), "r") as f:
                jargon_data = json.load(f)
                self.buzzwords = jargon_data["buzzwords"]
                self.job_titles = jargon_data["job_titles"]
                self.job_requirements = jargon_data["job_requirements"]
        except FileNotFoundError:
            print("Jargon file not found, using defaults")
            
    def generate_corporate_phrase(self):
        """Generate a random corporate jargon phrase"""
        templates = [
            "Let's {verb} our {adjective} {noun} to {verb} {adjective} {noun}.",
            "We need to {verb} the {adjective} {noun} to {verb} our {noun}.",
            "Our {adjective} {noun} will {verb} the {adjective} {noun}.",
            "I'd like to {verb} our {noun} to ensure we {verb} our {adjective} {noun}.",
            "Can we {verb} the {noun} to {verb} more {adjective} {noun}?",
            "{phrase} so we can {verb} our {adjective} {noun}."
        ]
        
        template = random.choice(templates)
        
        # Replace placeholders with random words
        while "{noun}" in template:
            template = template.replace("{noun}", random.choice(self.buzzwords["nouns"]), 1)
            
        while "{verb}" in template:
            template = template.replace("{verb}", random.choice(self.buzzwords["verbs"]), 1)
            
        while "{adjective}" in template:
            template = template.replace("{adjective}", random.choice(self.buzzwords["adjectives"]), 1)
            
        while "{phrase}" in template:
            template = template.replace("{phrase}", random.choice(self.buzzwords["phrases"]), 1)
            
        return template
        
    def generate_job_posting(self):
        """Generate a satirical job posting"""
        title = random.choice(self.job_titles)
        
        # Generate description
        description_templates = [
            "Looking for a {adjective} {noun} to join our {adjective} team!",
            "Are you a {adjective} {noun} who can {verb} our {noun}?",
            "Join our {adjective} team to {verb} the {noun} industry!",
            "We're disrupting the {noun} space and need a {adjective} rockstar!"
        ]
        
        description = random.choice(description_templates)
        
        # Replace placeholders
        while "{noun}" in description:
            description = description.replace("{noun}", random.choice(self.buzzwords["nouns"]), 1)
            
        while "{verb}" in description:
            description = description.replace("{verb}", random.choice(self.buzzwords["verbs"]), 1)
            
        while "{adjective}" in description:
            description = description.replace("{adjective}", random.choice(self.buzzwords["adjectives"]), 1)
            
        # Select 2-3 random requirements
        requirements = random.sample(self.job_requirements, random.randint(2, 3))
        
        return {
            "title": title,
            "description": description,
            "requirements": requirements
        }

# Generate corporate jargon if run directly
if __name__ == "__main__":
    generator = CorporateJargonGenerator()
    
    # Generate and print a sample phrase
    phrase = generator.generate_corporate_phrase()
    print("Corporate Phrase:", phrase)
    
    # Generate and print a sample job posting
    job = generator.generate_job_posting()
    print("\nJob Posting:")
    print(f"Title: {job['title']}")
    print(f"Description: {job['description']}")
    print("Requirements:")
    for req in job["requirements"]:
        print(f"- {req}")
