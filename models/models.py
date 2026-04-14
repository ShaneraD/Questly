from dataclasses import dataclass, field
from models.enums import QuestDifficuilty, QuestLength, QuestStatus, QuestType
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
    difficulty: QuestDifficuilty
    length: QuestLength
    quest_type: QuestType
    status: QuestStatus = QuestStatus.ACTIVE
    times_completed: int=0
    created_on: datetime
    completed_on: datetime = field()
