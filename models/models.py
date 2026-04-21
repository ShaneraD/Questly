from dataclasses import dataclass, field
from models.enums import QuestDifficulty, QuestLength, QuestStatus, QuestType
from datetime import datetime

@dataclass
class Player:
    name: str
    exp: int
    gold: int

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
    created_on: datetime = field(default_factory=datetime.now)
    completed_on: datetime | None = None

# Dataclass for Activity Log Entries