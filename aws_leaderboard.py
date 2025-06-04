#!/usr/bin/env python3
import boto3
import json
import uuid
import os
from datetime import datetime

class LeaderboardManager:
    def __init__(self, table_name="CorporateRunnerLeaderboard", region="us-east-1"):
        """Initialize the leaderboard manager with DynamoDB connection"""
        self.table_name = table_name
        self.region = region
        
        # Initialize DynamoDB client
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = None
        
        # Try to get the table, create it if it doesn't exist
        try:
            self.table = self.dynamodb.Table(table_name)
            self.table.table_status  # This will raise an exception if the table doesn't exist
        except:
            print(f"Table {table_name} does not exist. Please create it first.")
            print("You can run create_leaderboard_table() to create the table.")
            
    def create_leaderboard_table(self):
        """Create the leaderboard table in DynamoDB"""
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'player_id',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'timestamp',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'player_id',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'score',
                        'AttributeType': 'N'
                    }
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'ScoreIndex',
                        'KeySchema': [
                            {
                                'AttributeName': 'score',
                                'KeyType': 'HASH'
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            
            # Wait for the table to be created
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            self.table = table
            print(f"Table {self.table_name} created successfully")
            return True
        except Exception as e:
            print(f"Error creating table: {e}")
            return False
            
    def add_score(self, player_name, score, sector):
        """Add a new score to the leaderboard"""
        if not self.table:
            print("Table not initialized")
            return False
            
        try:
            timestamp = datetime.now().isoformat()
            player_id = str(uuid.uuid4())
            
            response = self.table.put_item(
                Item={
                    'player_id': player_id,
                    'player_name': player_name,
                    'score': score,
                    'sector': sector,
                    'timestamp': timestamp
                }
            )
            
            return True
        except Exception as e:
            print(f"Error adding score: {e}")
            return False
            
    def get_top_scores(self, limit=10):
        """Get the top scores from the leaderboard"""
        if not self.table:
            print("Table not initialized")
            return []
            
        try:
            response = self.table.scan(
                ProjectionExpression="player_name, score, sector, #ts",
                ExpressionAttributeNames={"#ts": "timestamp"},
                Limit=100  # Get more than we need for sorting
            )
            
            items = response.get('Items', [])
            
            # Sort by score in descending order
            sorted_items = sorted(items, key=lambda x: x['score'], reverse=True)
            
            # Return only the top N scores
            return sorted_items[:limit]
        except Exception as e:
            print(f"Error getting top scores: {e}")
            return []
            
    def save_local_score(self, player_name, score, sector):
        """Save score locally when offline"""
        local_scores = self.load_local_scores()
        
        timestamp = datetime.now().isoformat()
        player_id = str(uuid.uuid4())
        
        local_scores.append({
            'player_id': player_id,
            'player_name': player_name,
            'score': score,
            'sector': sector,
            'timestamp': timestamp
        })
        
        # Sort by score in descending order
        local_scores = sorted(local_scores, key=lambda x: x['score'], reverse=True)
        
        # Save to local file
        os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
        with open(os.path.join(os.path.dirname(__file__), "data", "local_scores.json"), "w") as f:
            json.dump(local_scores, f, indent=4)
            
        return True
        
    def load_local_scores(self, limit=10):
        """Load locally saved scores"""
        try:
            with open(os.path.join(os.path.dirname(__file__), "data", "local_scores.json"), "r") as f:
                local_scores = json.load(f)
                
            # Sort by score in descending order
            sorted_scores = sorted(local_scores, key=lambda x: x['score'], reverse=True)
            
            # Return only the top N scores
            return sorted_scores[:limit]
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading local scores: {e}")
            return []
            
    def sync_local_scores(self):
        """Sync locally saved scores to DynamoDB"""
        if not self.table:
            print("Table not initialized")
            return False
            
        try:
            local_scores = self.load_local_scores(limit=100)  # Get all local scores
            
            for score in local_scores:
                self.table.put_item(Item=score)
                
            # Clear local scores after syncing
            with open(os.path.join(os.path.dirname(__file__), "data", "local_scores.json"), "w") as f:
                json.dump([], f)
                
            return True
        except Exception as e:
            print(f"Error syncing local scores: {e}")
            return False

# Test the leaderboard manager if run directly
if __name__ == "__main__":
    leaderboard = LeaderboardManager()
    
    # Uncomment to create the table
    # leaderboard.create_leaderboard_table()
    
    # Save a local score
    leaderboard.save_local_score("TestPlayer", 1000, "TECH")
    
    # Get local scores
    local_scores = leaderboard.load_local_scores()
    print("Local Scores:")
    for score in local_scores:
        print(f"{score['player_name']}: {score['score']} ({score['sector']})")
