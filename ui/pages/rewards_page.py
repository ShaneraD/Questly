from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from logic.app_logic import AppLogic
from models.enums import QuestDifficulty, QuestLength


class RewardsPage(QWidget):
    def __init__(self, app_logic: AppLogic, main_window):
        super().__init__()
        self.app_logic = app_logic
        self.main_window = main_window

        layout = QVBoxLayout(self) 

        # labels to present information to the user - labels updated with methods below
        self.title_label = QLabel("Rewards")
        self.player_label = QLabel("Player reward information will appear here.")
        self.reward_formula_label = QLabel("Reward formula information will appear here.")
        self.difficulty_label = QLabel("Difficulty reward scaling")
        self.length_label = QLabel("Length reward scaling")
        self.future_rewards_label = QLabel("Future rewards, achievements, unlocks, or special progression features will be available for purchase with gold in the future.\nRoadmap: EXP and Luck potions, Avatar Customization, Additional Settings")

        layout.addWidget(self.title_label)

        # Add widgets to the layout
        layout.addWidget(self.player_label)
        layout.addWidget(self.reward_formula_label)
        layout.addWidget(self.difficulty_label)
        layout.addWidget(self.length_label)
        layout.addWidget(self.future_rewards_label)
        layout.addStretch()

        self.refresh()

    # Rewards refresh method
    def refresh(self) -> None:
        player = self.app_logic.get_player()
        # Display Player Data
        if player is not None:
            self.player_label.setText(f"Player: {player.name} | Level: {player.level} | Gold: {player.gold} | EXP: {player.experience}")

        self.reward_formula_label.setText(
            "Current reward formula: Base Gold = 10, Base EXP = 5, "
            "modified by quest difficulty and quest length.")
        # Table for difficulty modifiers as set in enums
        difficulty_lines = ["Difficulty Scaling:"]
        for difficulty in QuestDifficulty:
            difficulty_lines.append(f"- {difficulty.label}: x{difficulty.multiplier}")            
        self.difficulty_label.setText("\n".join(difficulty_lines))
        
        # Table for length modifiers as set in enums
        length_lines = ["Length Scaling:"]
        for length in QuestLength:
            length_lines.append(f"- {length.label}: x{length.multiplier}")
        self.length_label.setText("\n".join(length_lines))