from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        self.title_label = QLabel("Settings")

        layout.addWidget(self.title_label)
