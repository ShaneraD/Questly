from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QMessageBox,
    QLineEdit, QPushButton)

from logic.app_logic import AppLogic


class SettingsPage(QWidget):
    def __init__(self, app_logic: AppLogic, main_window):
        super().__init__()

        self.app_logic = app_logic
        self.main_window = main_window

        layout = QVBoxLayout(self)

        self.title_label = QLabel("Settings")
        self.description_label = QLabel(
            "These settings control simple Questly behavior and future interface options."
        )


        self.player_name_label = QLabel("Player Name")

        # Area for user to set player name outside of default "Hero"
        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Hero")

        self.save_player_name_button = QPushButton("Save Player Name")
        self.save_player_name_button.clicked.connect(self.save_player_name)

        player_name_layout = QHBoxLayout()
        player_name_layout.addWidget(self.player_name_input)
        player_name_layout.addWidget(self.save_player_name_button)

        self.confirm_delete_checkbox = QCheckBox("Require confirmation before deleting quests")
        self.confirm_delete_checkbox.setChecked(True)

        self.confirm_archive_checkbox = QCheckBox("Require confirmation before archiving quests")
        self.confirm_archive_checkbox.setChecked(False)

        self.completion_chime_checkbox = QCheckBox("Enable quest completion chime")
        self.completion_chime_checkbox.setChecked(False)

        self.compact_dashboard_checkbox = QCheckBox("Use compact dashboard display")
        self.compact_dashboard_checkbox.setChecked(False)

        # Note for the User - Will re-use this label for name change text.
        self.status_label = QLabel("Settings are currently using starter defaults.")

        self.confirm_delete_checkbox.toggled.connect(self._handle_setting_changed)
        self.confirm_archive_checkbox.toggled.connect(self._handle_setting_changed)
        self.completion_chime_checkbox.toggled.connect(self._handle_setting_changed)
        self.compact_dashboard_checkbox.toggled.connect(self._handle_setting_changed)

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)

        layout.addWidget(self.player_name_label)
        layout.addLayout(player_name_layout)

        layout.addWidget(self.confirm_delete_checkbox)
        layout.addWidget(self.confirm_archive_checkbox)
        layout.addWidget(self.completion_chime_checkbox)
        layout.addWidget(self.compact_dashboard_checkbox)
        layout.addWidget(self.status_label)
        layout.addStretch()

        self.refresh()

    # page specific refresh logic - player name text
    def refresh(self) -> None:
        player = self.app_logic.get_player()
        if player is not None:
            self.player_name_input.setText(player.name)
        else: 
            self.player_name_input.clear()
            self.player_name_input.setPlaceholderText("Hero")

    def save_player_name(self) -> None:
        try:
            updated_player = self.app_logic.update_player_name(self.player_name_input.text())
        except ValueError as error:
            QMessageBox.warning(self, "Player Update Error", str(error))
            return

        self.player_name_input.setText(updated_player.name)
        self.status_label.setText(f"Player name updated to {updated_player.name}.")

        self.main_window.refresh_after_data_change()

    def _handle_setting_changed(self) -> None:
        self.status_label.setText("Setting changed.")