from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton 

# Custom sidebar widget for the application

class Sidebar(QWidget):
    def __init__(self):
        # Initialize parent
        super().__init__()

        #QVBoxLayout to arrange buttons vertically
        layout = QVBoxLayout(self)

        # Create buttons for the sidebar and define labels
        self.dashboard_button = QPushButton("Dashboard")
        self.quests_button = QPushButton("Quests")
        self.activity_log_button = QPushButton("Activity Log")
        self.rewards_button = QPushButton("Rewards")
        self.settings_button = QPushButton("Settings")

        # Add buttons to the layout
        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.quests_button)
        layout.addWidget(self.rewards_button)
        layout.addWidget(self.activity_log_button)
        layout.addWidget(self.settings_button)
        
        layout.addStretch()  # Add stretch to push buttons to the top