#!/usr/bin/env python3
import json
import random
import os

class ObstacleGenerator:
    def __init__(self):
        self.patterns = {
            "skill_gap": [
                {"difficulty": "easy", "qte_count": 2, "time_limit": 1.5},
                {"difficulty": "medium", "qte_count": 3, "time_limit": 1.2},
                {"difficulty": "hard", "qte_count": 4, "time_limit": 1.0}
            ],
            "ats_laser": [
                {"difficulty": "easy", "pattern_length": 3, "time_per_key": 0.8},
                {"difficulty": "medium", "pattern_length": 4, "time_per_key": 0.6},
                {"difficulty": "hard", "pattern_length": 5, "time_per_key": 0.4}
            ],
            "experience_wall": [
                {"difficulty": "easy", "click_count": 3, "time_limit": 2.0},
                {"difficulty": "medium", "click_count": 5, "time_limit": 1.5},
                {"difficulty": "hard", "click_count": 7, "time_limit": 1.0}
            ]
        }
        
        # Ensure data directory exists
        os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
        
        # Save patterns to JSON file
        self.save_patterns()
        
    def save_patterns(self):
        """Save obstacle patterns to JSON file"""
        with open(os.path.join(os.path.dirname(__file__), "data", "obstacle_patterns.json"), "w") as f:
            json.dump(self.patterns, f, indent=4)
            
    def load_patterns(self):
        """Load obstacle patterns from JSON file"""
        try:
            with open(os.path.join(os.path.dirname(__file__), "data", "obstacle_patterns.json"), "r") as f:
                self.patterns = json.load(f)
        except FileNotFoundError:
            print("Patterns file not found, using defaults")
            
    def generate_obstacle_sequence(self, difficulty="medium", length=5):
        """Generate a sequence of obstacles with specified difficulty"""
        sequence = []
        
        for _ in range(length):
            obstacle_type = random.choice(list(self.patterns.keys()))
            
            # Find the pattern matching the requested difficulty
            pattern = next((p for p in self.patterns[obstacle_type] if p["difficulty"] == difficulty), 
                          self.patterns[obstacle_type][0])
            
            # Determine lane
            lane = random.randint(0, 2)
            
            # Create obstacle definition
            obstacle = {
                "type": obstacle_type,
                "lane": lane,
                "pattern": pattern
            }
            
            sequence.append(obstacle)
            
        return sequence
        
    def generate_balanced_sequence(self, player_score, length=10):
        """Generate a balanced sequence based on player score"""
        # Determine appropriate difficulty based on score
        if player_score < 300:
            difficulty = "easy"
        elif player_score < 700:
            difficulty = "medium"
        else:
            difficulty = "hard"
            
        # Generate sequence with appropriate difficulty
        sequence = self.generate_obstacle_sequence(difficulty, length)
        
        # Add some variety by occasionally inserting different difficulty obstacles
        for i in range(length):
            if random.random() < 0.2:  # 20% chance to change difficulty
                if difficulty == "easy":
                    alt_difficulty = "medium"
                elif difficulty == "hard":
                    alt_difficulty = "medium"
                else:
                    alt_difficulty = random.choice(["easy", "hard"])
                    
                obstacle_type = random.choice(list(self.patterns.keys()))
                pattern = next((p for p in self.patterns[obstacle_type] if p["difficulty"] == alt_difficulty), 
                              self.patterns[obstacle_type][0])
                
                lane = random.randint(0, 2)
                
                sequence[i] = {
                    "type": obstacle_type,
                    "lane": lane,
                    "pattern": pattern
                }
                
        return sequence

# Generate obstacle patterns if run directly
if __name__ == "__main__":
    generator = ObstacleGenerator()
    
    # Generate and print a sample sequence
    sequence = generator.generate_balanced_sequence(500, 5)
    print(json.dumps(sequence, indent=4))
