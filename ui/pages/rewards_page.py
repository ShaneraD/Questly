from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from models.enums import QuestDifficulty, QuestLength

class RewardsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.title_label = QLabel("Rewards")
        self.player_label = QLabel("Any Additional Player reward information can be added here.")
        self.reward_formula_label = QLabel("Current reward formula: Base Gold = 10, Base EXP = 5, modified by quest difficulty and quest length.")
        self.difficulty_label = QLabel("Difficulty reward scaling")
        self.length_label = QLabel("Length reward scaling")
        self.future_rewards_label = QLabel("Future rewards, achievements, unlocks, or special progression features can be displayed here.")

        layout.addWidget(self.title_label)
        layout.addWidget(self.player_label)
        layout.addWidget(self.reward_formula_label)
        layout.addWidget(self.difficulty_label)
        layout.addWidget(self.length_label)
        layout.addWidget(self.future_rewards_label)
        layout.addStretch()




