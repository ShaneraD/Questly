#Database management for the quest system
#This module handles all interactions with the SQLite database

import sqlite3
from pathlib import Path
from datetime import datetime

from models.enums import QuestDifficulty, QuestLength, QuestStatus, QuestType
from models.models import Player, Quest

# Class to manage database interactions
class DatabaseManager:
    # Create class constructor, should define path for SQLite database. data/app.db default, define for clarity
    def __init__(self,db_path: str = "data/app.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Method to get a connection to the SQLite database
    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row #Access row by column name
        return conn

    #Method to initialize the database, creating necessary tables if they don't exist
    def initialize_database(self) -> None:
        with self.get_connection() as conn: 
            cursor = conn.cursor() #cursor object to execute SQL commands

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                gold INTEGER NOT NULL DEFAULT 0,
                experience INTEGER NOT NULL DEFAULT 0
                       )
                    """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                length TEXT NOT NULL,
                quest_type TEXT NOT NULL,
                status TEXT NOT NULL,
                times_completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                completed_at TEXT
                           )     
        
                    """)
            
            cursor.execute("SELECT count(*) FROM player")
            player_count = cursor.fetchone()[0]

            if player_count == 0:
                cursor.execute("""
                    INSERT INTO player (name, level, gold, experience) VALUES (?, ?, ?, ?)
                    """, ("Hero", 1, 0, 0))
                
                conn.commit()
        
    #----------------------
    # Player methods

    #Method to get player data from the database, returns a Player object

    #Method to update player data in the database, takes a Player object as input

    #----------------------
    #Quest methods

    #Method to create a new quest in the database, takes a Quest object as input

    #Methods to get quests from the database, optional filters, will at least want to be able to return all or active quests

    #Method to update quest data in the database, takes a Quest object as input

    #Method to delete a quest from the database, takes a quest ID as input

    #----------------------
    #Additional methods as needed