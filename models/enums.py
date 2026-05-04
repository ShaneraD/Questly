from enum import Enum

class QuestDifficulty(Enum):
    EASY = ("Easy",1.0)
    NORMAL = ("Normal",1.25)
    HARD = ("Hard",1.5)

    def __init__(self, label: str, multiplier: float):
        self.label = label
        self.multiplier = multiplier

class QuestLength(Enum):
    SHORT = ("Short", 1.0)
    MEDIUM = ("Medium", 1.5)
    LONG = ("Long", 2.0)

    def __init__(self, label: str, multiplier: float):
        self.label = label
        self.multiplier = multiplier

    #FUTURE: add Daily, Weekly
class QuestType(Enum):
    ONE_TIME = "One-Time"
    REPEATABLE = "Repeatable"

    #FUTURE:Currently deleted quests are truly deleted, references in activity log are set to null. 
    #We might consider changing Delete to be an 'Invisible Status'
class QuestStatus(Enum):
    ACTIVE = "Active"
    COMPLETED ="Completed"
    ARCHIVED = "Archived"