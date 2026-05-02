from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLineEdit, QTextEdit, 
    QPushButton, QListWidget, QLabel,
    QMessageBox, QComboBox, QCheckBox,)

from logic.app_logic import AppLogic
from models.enums import QuestDifficulty, QuestLength, QuestType, QuestStatus
from models.models import Quest
from ui.dialogs import confirm_delete, EditQuestDialog


class QuestsPage(QWidget):
    def __init__(self, app_logic: AppLogic, main_window):
        super().__init__()

        self.app_logic = app_logic
        self.main_window = main_window
        self.selected_quest = None
        self.all_quests = []
        self.filtered_quests = []

        main_layout = QHBoxLayout(self)

        left_panel = QVBoxLayout()
        center_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # -------------------------
        # Quest creation form
        # -------------------------
        left_panel.addWidget(QLabel("Create New Quest"))

        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()

        self.difficulty_input = QComboBox()
        self.difficulty_input.addItems([difficulty.label for difficulty in QuestDifficulty])

        self.length_input = QComboBox()
        self.length_input.addItems([length.label for length in QuestLength])

        self.type_input = QComboBox()
        self.type_input.addItems([quest_type.value for quest_type in QuestType])

        self.add_button = QPushButton("Add Quest")
        self.add_button.clicked.connect(self.add_quest)

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Difficulty:", self.difficulty_input)
        form_layout.addRow("Length:", self.length_input)
        form_layout.addRow("Quest Type:", self.type_input)

        left_panel.addLayout(form_layout)
        left_panel.addWidget(self.add_button)
        left_panel.addStretch()

        # -------------------------
        # Quest list + filters
        # -------------------------
        center_panel.addWidget(QLabel("Quest Log"))

        self.show_active_checkbox = QCheckBox("Show Active")
        self.show_completed_checkbox = QCheckBox("Show Completed")
        self.show_archived_checkbox = QCheckBox("Show Archived")

        self.show_active_checkbox.setChecked(True)
        self.show_completed_checkbox.setChecked(False)
        self.show_archived_checkbox.setChecked(False)

        self.show_active_checkbox.toggled.connect(self.refresh)
        self.show_completed_checkbox.toggled.connect(self.refresh)
        self.show_archived_checkbox.toggled.connect(self.refresh)



        self.quest_list = QListWidget()
        self.quest_list.itemClicked.connect(self.select_quest)

        center_panel.addWidget(self.quest_list)

        center_panel.addWidget(self.show_active_checkbox)
        center_panel.addWidget(self.show_completed_checkbox)
        center_panel.addWidget(self.show_archived_checkbox)

        self.summary_label = QLabel("Quest Summary")
        center_panel.addWidget(self.summary_label)

        # -------------------------
        # Selected quest detail
        # -------------------------
        right_panel.addWidget(QLabel("Selected Quest Details"))
        self.detail_label = QLabel("Select a quest to view details.")
        self.detail_label.setWordWrap(True)
        self.complete_button = QPushButton("Complete Quest")
        self.edit_button = QPushButton("Edit Quest")
        self.archive_button = QPushButton("Archive Quest")
        self.delete_button = QPushButton("Delete Quest")

        self.complete_button.clicked.connect(self.complete_quest)
        self.edit_button.clicked.connect(self.edit_quest)
        self.archive_button.clicked.connect(self.archive_quest)
        self.delete_button.clicked.connect(self.delete_quest)

        right_panel.addWidget(self.detail_label)
        right_panel.addWidget(self.complete_button)
        right_panel.addWidget(self.edit_button)
        right_panel.addWidget(self.archive_button)
        right_panel.addWidget(self.delete_button)
        right_panel.addStretch()

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(center_panel, 1)
        main_layout.addLayout(right_panel, 1)

        self.refresh()

    def refresh(self) -> None:
        self.all_quests = self.app_logic.get_all_quests()
        self.filtered_quests = self._apply_filters(self.all_quests)

        self.quest_list.clear()
        for quest in self.filtered_quests:
            self.quest_list.addItem(f"{quest.title} [{quest.status.value}]")

        active_count = len([quest for quest in self.all_quests if quest.status == QuestStatus.ACTIVE])
        completed_count = len([quest for quest in self.all_quests if quest.status == QuestStatus.COMPLETED])
        archived_count = len([quest for quest in self.all_quests if quest.status == QuestStatus.ARCHIVED])

        self.summary_label.setText(
            f"Quest Summary | Active: {active_count} | Completed: {completed_count} | Archived: {archived_count}"
        )

        

        if self.selected_quest is not None:
            refreshed_quest = self.app_logic.get_quest_by_id(self.selected_quest.id)
            visible_ids = {quest.id for quest in self.filtered_quests}

            if refreshed_quest is None:
                self.selected_quest = None
                self.detail_label.setText("Select a quest to view details.")
            elif refreshed_quest.id not in visible_ids:
                self.selected_quest = None
                self.detail_label.setText("Select a quest to view details.")
            else:
                self.selected_quest = refreshed_quest
                self._update_detail_label()

    def _apply_filters(self, quests: list[Quest]) -> list[Quest]:
        filtered = []

        for quest in quests:
            if quest.status == QuestStatus.ACTIVE and self.show_active_checkbox.isChecked():
                filtered.append(quest)
            elif quest.status == QuestStatus.COMPLETED and self.show_completed_checkbox.isChecked():
                filtered.append(quest)
            elif quest.status == QuestStatus.ARCHIVED and self.show_archived_checkbox.isChecked():
                filtered.append(quest)

        return filtered

    def add_quest(self) -> None:
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Validation Error", "Quest title is required.")
            return

        if not description:
            QMessageBox.warning(self, "Validation Error", "Quest description is required.")
            return

        difficulty = self._difficulty_from_label(self.difficulty_input.currentText())
        length = self._length_from_label(self.length_input.currentText())
        quest_type = QuestType(self.type_input.currentText())

        quest = Quest(
            id=None,
            title=title,
            description=description,
            difficulty=difficulty,
            length=length,
            quest_type=quest_type,
        )

        self.app_logic.create_quest(quest)

        self.title_input.clear()
        self.description_input.clear()

        self.main_window.refresh_after_data_change()

    def select_quest(self, item) -> None:
        index = self.quest_list.row(item)
        self.selected_quest = self.filtered_quests[index]
        self._update_detail_label()

    def _update_detail_label(self) -> None:
        if self.selected_quest is None:
            self.detail_label.setText("Select a quest to view details.")
            return

        reward_gold, reward_experience = self.app_logic.calculate_rewards(self.selected_quest)

        completed_at_text = (
            self.selected_quest.completed_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.selected_quest.completed_at
            else "Never"
        )

        self.detail_label.setText(
            f"Title: {self.selected_quest.title}\n"
            f"Description: {self.selected_quest.description}\n"
            f"Difficulty: {self.selected_quest.difficulty.label}\n"
            f"Length: {self.selected_quest.length.label}\n"
            f"Type: {self.selected_quest.quest_type.value}\n"
            f"Status: {self.selected_quest.status.value}\n"
            f"Times completed: {self.selected_quest.times_completed}\n"
            f"Last completed: {completed_at_text}\n"
            f"Reward: {reward_gold} Gold, {reward_experience} EXP"
        )

    def complete_quest(self) -> None:
        if self.selected_quest is None:
            QMessageBox.warning(self, "No Quest Selected", "Please select a quest first.")
            return

        try:
            updated_quest, updated_player, reward_gold, reward_experience = self.app_logic.complete_quest(self.selected_quest.id)
        except ValueError as error:
            QMessageBox.warning(self, "Quest Completion Error", str(error))
            self.main_window.refresh_after_data_change()
        return

        self.selected_quest = updated_quest
        self.main_window.refresh_after_data_change()

        QMessageBox.information(
            self,
            "Quest Completed",
            f"Completed '{updated_quest.title}'\n"
            f"+{reward_gold} Gold\n"
            f"+{reward_experience} EXP\n"
            f"Player Gold: {updated_player.gold}\n"
            f"Player EXP: {updated_player.experience}"
        )

    def edit_quest(self) -> None:
        if self.selected_quest is None:
            QMessageBox.warning(self, "No Quest Selected", "Please select a quest first.")
            return

        dialog = EditQuestDialog(self.selected_quest, self)

        if dialog.exec():
            updated_values = dialog.get_updated_values()

            if not updated_values["title"]:
                QMessageBox.warning(self, "Validation Error", "Quest title is required.")
                return

            if not updated_values["description"]:
                QMessageBox.warning(self, "Validation Error", "Quest description is required.")
                return

            self.selected_quest.title = updated_values["title"]
            self.selected_quest.description = updated_values["description"]
            self.selected_quest.difficulty = self._difficulty_from_label(updated_values["difficulty_label"])
            self.selected_quest.length = self._length_from_label(updated_values["length_label"])
            self.selected_quest.quest_type = QuestType(updated_values["quest_type_value"])

            self.app_logic.update_quest(self.selected_quest)
            self.main_window.refresh_after_data_change()

    def archive_quest(self) -> None:
        if self.selected_quest is None:
            QMessageBox.warning(self, "No Quest Selected", "Please select a quest first.")
            return

        self.app_logic.archive_quest(self.selected_quest.id)
        self.selected_quest = None
        self.main_window.refresh_after_data_change()

    def delete_quest(self) -> None:
        if self.selected_quest is None:
            QMessageBox.warning(self, "No Quest Selected", "Please select a quest first.")
            return

        if confirm_delete(self, self.selected_quest.title):
            self.app_logic.delete_quest(self.selected_quest.id)
            self.selected_quest = None
            self.main_window.refresh_after_data_change()

    def _difficulty_from_label(self, label: str) -> QuestDifficulty:
        for difficulty in QuestDifficulty:
            if difficulty.label == label:
                return difficulty
        raise ValueError(f"Unknown difficulty label: {label}")

    def _length_from_label(self, label: str) -> QuestLength:
        for length in QuestLength:
            if length.label == label:
                return length
        raise ValueError(f"Unknown length label: {label}")