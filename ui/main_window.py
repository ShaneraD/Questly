from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from logic.app_logic import AppLogic
from ui.sidebar import Sidebar

from ui.pages.dashboard_page import DashboardPage
from ui.pages.quests_page import QuestsPage
from ui.pages.settings_page import SettingsPage
from ui.pages.rewards_page import RewardsPage
from ui.pages.activity_log_page import ActivityLogPage

class MainWindow(QMainWindow):
    def __init__(self, app_logic: AppLogic):
        super().__init__()
        
        self.app_logic = app_logic

        # Define the main window properties
        self.setWindowTitle("Questly")
        self.resize(600, 400)
        
        # Add sidebar widget
        self.sidebar = Sidebar()
        # Widget that allows stacking widgets on top of each other, only showing one at a time (Page switching)
        self.stack = QStackedWidget()

        # add pages to MainWindow
        self.dashboard_page = DashboardPage(self.app_logic, self)
        self.quests_page = QuestsPage(self.app_logic, self)
        self.settings_page = SettingsPage(self.app_logic, self)
        self.rewards_page = RewardsPage(self.app_logic, self)
        self.activity_log_page = ActivityLogPage(self.app_logic, self)

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

    def _connect_sidebar(self) -> None:
        self.sidebar.dashboard_button.clicked.connect(lambda: self.switch_page(self.dashboard_page))
        self.sidebar.quests_button.clicked.connect(lambda: self.switch_page(self.quests_page))
        self.sidebar.rewards_button.clicked.connect(lambda: self.switch_page(self.rewards_page))
        self.sidebar.activity_log_button.clicked.connect(lambda: self.switch_page(self.activity_log_page))
        self.sidebar.settings_button.clicked.connect(lambda: self.switch_page(self.settings_page))

    def switch_page(self, page: QWidget) -> None:
        self.stack.setCurrentWidget(page)

        if hasattr(page, "refresh"):
            page.refresh()

    def refresh_sidebar(self) -> None:
        player = self.app_logic.get_player()
        self.sidebar.update_player_display(player)

    def refresh_all_pages(self) -> None:
        self.refresh_sidebar()

        for page in [
            self.dashboard_page,
            self.quests_page,
            self.activity_log_page,
            self.rewards_page,
            self.settings_page,
        ]:
            if hasattr(page, "refresh"):
                page.refresh()

    def refresh_after_data_change(self) -> None:
        self.refresh_sidebar()
        self.dashboard_page.refresh()
        self.quests_page.refresh()
        self.activity_log_page.refresh()
        self.rewards_page.refresh()