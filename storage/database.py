from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime

from models.enums import QuestDifficulty, QuestLength, QuestType, QuestStatus
from models.models import Player, Quest, ActivityLogEntry


class DatabaseManager:
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize_database(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # currently application assumes a single player, built with potential for multiple user profiles in future versions.
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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quest_id INTEGER,
                    quest_title TEXT NOT NULL,
                    reward_gold INTEGER NOT NULL,
                    reward_experience INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (quest_id) REFERENCES quests(id) ON DELETE SET NULL
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM player")
            player_count = cursor.fetchone()[0]

            if player_count == 0:
                cursor.execute("""
                    INSERT INTO player (name, level, gold, experience)
                    VALUES (?, ?, ?, ?)
                """, ("Hero", 1, 0, 0))

            conn.commit()

    # -------------------------
    # Player methods
    # -------------------------

    def get_player(self) -> Player | None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, level, gold, experience
                FROM player
                LIMIT 1
            """)
            row = cursor.fetchone()

        if row is None:
            return None

        return Player(
            id=row["id"],
            name=row["name"],
            level=row["level"],
            gold=row["gold"],
            experience=row["experience"]
        )

    def update_player(self, player: Player) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE player
                SET name = ?,
                    level = ?,
                    gold = ?,
                    experience = ?
                WHERE id = ?
            """, (
                player.name,
                player.level,
                player.gold,
                player.experience,
                player.id
            ))
            conn.commit()

    # -------------------------
    # Quest methods
    # -------------------------

    def add_quest(self, quest: Quest) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO quests (
                    title,
                    description,
                    difficulty,
                    length,
                    quest_type,
                    status,
                    times_completed,
                    created_at,
                    completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                quest.title,
                quest.description,
                quest.difficulty.name,
                quest.length.name,
                quest.quest_type.value,
                quest.status.value,
                quest.times_completed,
                quest.created_at.isoformat(),
                quest.completed_at.isoformat() if quest.completed_at else None
            ))
            conn.commit()
            return cursor.lastrowid
    # Full Quest List
    def get_all_quests(self) -> list[Quest]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM quests
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()

        return [self._row_to_quest(row) for row in rows]
    # method to return active quests - dashboard view
    def get_active_quests(self) -> list[Quest]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM quests
                WHERE status = ?
                ORDER BY created_at DESC
            """, (QuestStatus.ACTIVE.value,))
            rows = cursor.fetchall()

        return [self._row_to_quest(row) for row in rows]

    #Method to pull quest by status
    def get_quests_by_status(self, status: QuestStatus) -> list[Quest]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM quests
                WHERE status = ?
                ORDER BY created_at DESC
            """, (status.value,))
            rows = cursor.fetchall()

        return [self._row_to_quest(row) for row in rows]

    def get_quest_by_id(self, quest_id: int) -> Quest | None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM quests
                WHERE id = ?
            """, (quest_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_quest(row)
    # Method to update quest in Database - Takes Quest as input
    def update_quest(self, quest: Quest) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE quests
                SET title = ?,
                    description = ?,
                    difficulty = ?,
                    length = ?,
                    quest_type = ?,
                    status = ?,
                    times_completed = ?,
                    created_at = ?,
                    completed_at = ?
                WHERE id = ?
            """, (
                quest.title,
                quest.description,
                quest.difficulty.name,
                quest.length.name,
                quest.quest_type.value,
                quest.status.value,
                quest.times_completed,
                quest.created_at.isoformat(),
                quest.completed_at.isoformat() if quest.completed_at else None,
                quest.id
            ))
            conn.commit()

    def delete_quest(self, quest_id: int) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM quests
                WHERE id = ?
            """, (quest_id,))
            conn.commit()

    # -------------------------
    # Activity log methods
    # -------------------------

    def add_activity_log_entry(self, entry: ActivityLogEntry) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activity_log (
                    quest_id,
                    quest_title,
                    reward_gold,
                    reward_experience,
                    completed_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                entry.quest_id,
                entry.quest_title,
                entry.reward_gold,
                entry.reward_experience,
                entry.completed_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid

    def get_recent_activity(self, limit: int = 10) -> list[ActivityLogEntry]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM activity_log
                ORDER BY completed_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        return [self._row_to_activity_log_entry(row) for row in rows]

    # -------------------------
    # private helper methods
    # -------------------------
    
    def _row_to_quest(self, row: sqlite3.Row) -> Quest:
        return Quest(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            difficulty=QuestDifficulty[row["difficulty"]],
            length=QuestLength[row["length"]],
            quest_type=QuestType(row["quest_type"]),
            status=QuestStatus(row["status"]),
            times_completed=row["times_completed"],
            created_at=datetime.fromisoformat(row["created_at"]),
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None)
    
    def _row_to_activity_log_entry(self, row: sqlite3.Row) -> ActivityLogEntry:
        return ActivityLogEntry(
            id=row["id"],
            quest_id=row["quest_id"],
            quest_title=row["quest_title"],
            reward_gold=row["reward_gold"],
            reward_experience=row["reward_experience"],
            completed_at=datetime.fromisoformat(row["completed_at"]))