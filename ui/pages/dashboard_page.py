from PySide6.QTWidgets import QWidget, QVBoxLayout, QLabel

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout(self)

        self.title_label = QLabel("Dashboard:")
    
        layout.addWidget(self.title_label)