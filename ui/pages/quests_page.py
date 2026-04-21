from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class QuestsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        self.title_label = QLabel("Quests")

        layout.addWidget(self.title_label)
