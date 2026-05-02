from PySide6.QtWidgets import (
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDialogButtonBox,
)

from models.enums import QuestDifficulty, QuestLength, QuestType
from models.models import Quest


def confirm_delete(parent, item_name="this item"):
    reply = QMessageBox.question(
        parent,
        "Confirm Delete",
        f"Are you sure you want to delete {item_name}?",
        QMessageBox.Yes | QMessageBox.No
    )
    return reply == QMessageBox.Yes


class EditQuestDialog(QDialog):
    def __init__(self, quest: Quest, parent=None):
        super().__init__(parent)

        self.quest = quest
        self.setWindowTitle("Edit Quest")
        self.resize(400, 300)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.title_input = QLineEdit(quest.title)
        self.description_input = QTextEdit()
        self.description_input.setPlainText(quest.description)

        self.difficulty_input = QComboBox()
        self.difficulty_input.addItems([difficulty.label for difficulty in QuestDifficulty])
        self.difficulty_input.setCurrentText(quest.difficulty.label)

        self.length_input = QComboBox()
        self.length_input.addItems([length.label for length in QuestLength])
        self.length_input.setCurrentText(quest.length.label)

        self.type_input = QComboBox()
        self.type_input.addItems([quest_type.value for quest_type in QuestType])
        self.type_input.setCurrentText(quest.quest_type.value)

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Difficulty:", self.difficulty_input)
        form_layout.addRow("Length:", self.length_input)
        form_layout.addRow("Quest Type:", self.type_input)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

    def get_updated_values(self) -> dict:
        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "difficulty_label": self.difficulty_input.currentText(),
            "length_label": self.length_input.currentText(),
            "quest_type_value": self.type_input.currentText(),
        }