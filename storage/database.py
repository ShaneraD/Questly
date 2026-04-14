import sqlite3
from pathlib import Path
from datetime import datetime

from models.enums import QuestDifficulty, QuestLength, QuestStatus, QuestType
from models.models import Player, Quest

class DatabaseManager:

    def initialize_database(self) -> None:
        cursor = conn.cursor()

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
                
                    """)