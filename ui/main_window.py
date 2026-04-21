from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from ui.sidebar import Sidebar

from ui.pages.dashboard_page import DashboardPage
from ui.pages.quests_page import QuestsPage
from ui.pages.settings_page import SettingsPage
from ui.pages.rewards_page import RewardsPage
from ui.pages.activity_log_page import ActivityLogPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define the main window properties
        self.setWindowTitle("Questly")
        self.resize(800, 600)
        
        # Add sidebar widget
        self.sidebar = Sidebar()
        # Widget that allows stacking widgets on top of each other, only showing one at a time (Page switching)
        self.stack = QStackedWidget()

        # add pages to MainWindow
        self.dashboard_page = DashboardPage(self)
        self.quests_page = QuestsPage(self)
        self.settings_page = SettingsPage(self)
        self.rewards_page = RewardsPage(self)
        self.activity_log_page = ActivityLogPage(self)

        # Add pages to the stack
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.quests_page)
        self.stack.addWidget(self.rewards_page)
        self.stack.addWidget(self.activity_log_page)
        self.stack.addWidget(self.settings_page)

        self._connect_sidebar()
        
        container = QWidget()
        layout = QHBoxLayout(container)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)

        self.setCentralWidget(container)

        self.refresh_all_pages()


    def _connect_sidebar(self)-> None:
        self.sidebar.dashboard_button.clicked.connect(lambda: self.switch_page(0))
        self.sidebar.quests_button.clicked.connect(lambda: self.switch_page(1))
        self.sidebar.rewards_button.clicked.connect(lambda: self.switch_page(2))
        self.sidebar.activity_log_button.clicked.connect(lambda: self.switch_page(3))
        self.sidebar.settings_button.clicked.connect(lambda: self.switch_page(4))

    def switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

    def refresh_all_pages(self) -> None:
        self.dashboard_page.refresh()

# Create method to refresh all pages when data changes