from dataclasses import dataclass, field
from models.enums import QuestDifficulty, QuestLength, QuestStatus, QuestType
from datetime import datetime

@dataclass
class Player:
    id: int | None
    level: int
    name: str
    gold: int
    experience: int

@dataclass
class Quest:
    id: int | None
    title: str
    description: str
    difficulty: QuestDifficulty
    length: QuestLength
    quest_type: QuestType
    status: QuestStatus = QuestStatus.ACTIVE
    times_completed: int=0
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

@dataclass
class ActivityLogEntry:
    id: int | None
    quest_id: int
    quest_title: str
    reward_gold: int
    reward_experience: int
    completed_at: datetime = field(default_factory=datetime.now)