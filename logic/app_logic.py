from datetime import datetime

from models.enums import QuestStatus, QuestType
from models.models import Quest, ActivityLogEntry, Player
from storage.database import DatabaseManager

class AppLogic:
    def __init__(self, db: DatabaseManager):
        self.db = db

    # -------------------------
    # Reward / progression logic
    # -------------------------
    
    #Calculate rewards - base values by multipliers
    def calculate_rewards(self, quest: Quest) -> tuple[int, int]:
        base_gold = 10
        base_experience = 5

        gold = int(base_gold * quest.difficulty.multiplier * quest.length.multiplier)
        experience = int(base_experience * quest.difficulty.multiplier * quest.length.multiplier)

        return gold, experience
    #Currently extremely simple formula for testing, level should go up every 100 experience 
    def calculate_level(self, experience: int) -> int:
        return max(1, experience // 100 + 1)

    def apply_rewards_to_player(self, reward_gold: int, reward_experience: int) -> Player:
        player = self.db.get_player()
        if player is None:
            raise ValueError("No player found in database.")

        player.gold += reward_gold
        player.experience += reward_experience
        player.level = self.calculate_level(player.experience)

        self.db.update_player(player)
        return player

    # -------------------------
    # Quest CRUD methods
    # -------------------------

    def create_quest(self, quest: Quest) -> int:
        return self.db.add_quest(quest)

    def get_all_quests(self) -> list[Quest]:
        return self.db.get_all_quests()

    def get_active_quests(self) -> list[Quest]:
        return self.db.get_active_quests()

    def get_quest_by_id(self, quest_id: int) -> Quest | None:
        return self.db.get_quest_by_id(quest_id)

    def update_quest(self, quest: Quest) -> None:
        self.db.update_quest(quest)

    def delete_quest(self, quest_id: int) -> None:
        self.db.delete_quest(quest_id)

    def archive_quest(self, quest_id: int) -> None:
        quest = self.db.get_quest_by_id(quest_id)
        if quest is None:
            raise ValueError(f"No quest found with id {quest_id}")
        
        quest.status = QuestStatus.ARCHIVED
        self.db.update_quest(quest)

    # -------------------------
    # Quest workflow logic
    # -------------------------

    # Currently opens multiple connections to the database, which commit independently.
    # In the future, we may want to refactor here to use a single transaction for the workflow, but this functions for our working model

    def complete_quest(self, quest_id: int) -> tuple[Quest, Player, int, int]:
        quest = self.db.get_quest_by_id(quest_id)       
        if quest is None:
            raise ValueError(f"No quest found with id {quest_id}")

        if quest.status != QuestStatus.ACTIVE:
            raise ValueError("Only active quests can be completed.")

        reward_gold, reward_experience = self.calculate_rewards(quest)

        now = datetime.now()
        quest.times_completed += 1
        quest.completed_at = now

        if quest.quest_type == QuestType.ONE_TIME:
            quest.status = QuestStatus.COMPLETED
        elif quest.quest_type == QuestType.REPEATABLE:
            quest.status = QuestStatus.ACTIVE

        self.db.update_quest(quest)

        updated_player = self.apply_rewards_to_player(reward_gold, reward_experience)

        log_entry = ActivityLogEntry(
            id=None,
            quest_id=quest.id,
            quest_title=quest.title,
            reward_gold=reward_gold,
            reward_experience=reward_experience,
            completed_at=now
        )
        self.db.add_activity_log_entry(log_entry)

        return quest, updated_player, reward_gold, reward_experience

    # -------------------------
    # Dashboard / activity helper methods
    # -------------------------

    def get_player(self) -> Player | None:
        return self.db.get_player()
    
    def update_player_name(self, name: str) -> Player:
        player = self.db.get_player()

        if player is None:
            raise ValueError("No player found in database.")

        cleaned_name = name.strip()

        if not cleaned_name:
            cleaned_name = "Hero"

        player.name = cleaned_name
        self.db.update_player(player)

        return player    

    def get_recent_activity(self, limit: int = 10) -> list[ActivityLogEntry]:
        return self.db.get_recent_activity(limit)

    def get_dashboard_data(self) -> dict:
        player = self.db.get_player()
        all_quests = self.db.get_all_quests()
        active_quests = self.db.get_active_quests()
        recent_activity = self.db.get_recent_activity(limit=10)

        completed_count = len([quest for quest in all_quests if quest.status == QuestStatus.COMPLETED])

        oldest_active_quest = "None"
        if active_quests:
            oldest = min(active_quests, key=lambda quest: quest.created_at)
            oldest_active_quest = oldest.title

        stats = {
            "active_quests": len(active_quests),
            "total_completed": completed_count,
            "oldest_active_quest": oldest_active_quest,
            "recent_activity_count": len(recent_activity),
        }

        return {
            "player": player,
            "active_quests": active_quests,
            "recent_activity": recent_activity,
            "stats": stats,
        }