from enum import Enum

class QuestDifficulty(Enum):
    EASY = ("Easy",1.0)
    NORMAL = ("Normal",1.25)
    HARD = ("Hard",1.5)

class QuestLength(Enum):
    SHORT = ("Short")
    MEDIUM = ("Medium")
    LONG = ("Long")

class QuestType(Enum):
    ONE_TIME = "One-Time"
    REPEATABLE = "Repeatable"

class QuestStatus(Enum):
    ACTIVE = "Active"
    COMPLETE = "Complete"
    ARCHIVED = "Archived"