from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).resolve().parent.parent
        self.assets_dir = self.base_dir / "assets"

        layout = QVBoxLayout(self)
        # Avatar at the top
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setFixedSize(96, 96)
        #Character Info labels - values update on refresh
        self.name_label = QLabel("Character Name")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.level_label = QLabel("Level: ")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #Created rows for the XP and Gold on the sidebar - to keep aligned with images
        xp_row = QHBoxLayout()
        xp_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.xp_icon_label = QLabel()
        self.xp_icon_label.setFixedSize(16, 16)
        self.xp_value_label = QLabel("XP: 0")

        xp_row.addWidget(self.xp_icon_label)
        xp_row.addWidget(self.xp_value_label)

        gold_row = QHBoxLayout()
        gold_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gold_icon_label = QLabel()
        self.gold_icon_label.setFixedSize(16, 16)
        self.gold_value_label = QLabel("Gold: 0")

        gold_row.addWidget(self.gold_icon_label)
        gold_row.addWidget(self.gold_value_label)

        # set images
        self._set_avatar(self.assets_dir / "knight.gif")

        self._set_gif_icon(self.xp_icon_label, self.assets_dir / "bluecoin.gif")
        self._set_gif_icon(self.gold_icon_label, self.assets_dir / "coin.gif")

        #add widgets to sidebar for player display
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.level_label)
        layout.addLayout(xp_row)
        layout.addLayout(gold_row)

        #define and add widgets for navigation
        self.dashboard_button = QPushButton("Dashboard")
        self.quests_button = QPushButton("Quests")
        self.activity_log_button = QPushButton("Activity Log")
        self.rewards_button = QPushButton("Rewards")
        self.settings_button = QPushButton("Settings")

        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.quests_button)
        layout.addWidget(self.rewards_button)
        layout.addWidget(self.activity_log_button)
        layout.addWidget(self.settings_button)

        layout.addStretch()
        
    # method to update labels to accurate player data
    def update_player_display(self, player) -> None:
        if player is None:
            self.name_label.setText("No Character")
            self.level_label.setText("Level: --")
            self.xp_value_label.setText("XP: --")
            self.gold_value_label.setText("Gold: --")
            return

        self.name_label.setText(player.name)
        self.level_label.setText(f"Level: {player.level}")
        self.xp_value_label.setText(f"XP: {player.experience}")
        self.gold_value_label.setText(f"Gold: {player.gold}")


    def _set_avatar(self, gif_path: Path) -> None:
        if not gif_path.exists():
            self.avatar_label.setText("No Avatar")
            return
        # start avatar .gif playback
        movie = QMovie(str(gif_path))
        movie.setScaledSize(QSize(96, 96))

        self.avatar_label.setMovie(movie)
        movie.start()

        if not hasattr(self, "_movies"):
            self._movies = []
        self._movies.append(movie)

    def _set_gif_icon(self, label: QLabel, gif_path: Path) -> None:
        if not gif_path.exists():
            return
        # start coin .gif playback
        movie = QMovie(str(gif_path))
        movie.setScaledSize(QSize(16, 16))
        label.setMovie(movie)
        movie.start()

        if not hasattr(self, "_movies"):
            self._movies = []
        self._movies.append(movie)