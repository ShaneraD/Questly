from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox

from logic.app_logic import AppLogic


class DashboardPage(QWidget):
    def __init__(self, app_logic: AppLogic, main_window):
        super().__init__()

        self.app_logic = app_logic
        self.main_window = main_window
        self.selected_quest = None
        self.active_quests = []

        # Layout for dashoard Two Vertical Boxes aligned Horizontally 
        main_layout = QHBoxLayout(self)

        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # Player summary at the top
        self.player_label = QLabel("Player Info")
        self.stats_label = QLabel("Quick Stats")

        left_panel.addWidget(QLabel("Dashboard"))
        left_panel.addWidget(self.player_label)
        left_panel.addWidget(self.stats_label)

        # -------------------------
        # Active quest preview
        # -------------------------
        left_panel.addWidget(QLabel("Active Quest Preview"))

        self.active_quest_list = QListWidget()
        self.active_quest_list.itemClicked.connect(self.select_quest)

        left_panel.addWidget(self.active_quest_list)

        # -------------------------
        # Recent activity
        # -------------------------
        left_panel.addWidget(QLabel("Recent Activity"))

        self.activity_list = QListWidget()
        left_panel.addWidget(self.activity_list)

        # -------------------------
        # Selected quest details
        # -------------------------

        # detail_label will update when a quest is selected
        right_panel.addWidget(QLabel("Selected Quest Details"))
        self.detail_label = QLabel("Select an active quest to view details.")
        self.detail_label.setWordWrap(True)
        self.quick_complete_button = QPushButton("Quick Complete Quest")
        self.quick_complete_button.clicked.connect(self.quick_complete_selected_quest)

        right_panel.addWidget(self.detail_label)
        right_panel.addWidget(self.quick_complete_button)
        right_panel.addStretch()

        main_layout.addLayout(left_panel, 2)
        main_layout.addLayout(right_panel, 1)

        self.refresh()
    #Dashboard refresh method
    def refresh(self) -> None:
        dashboard_data = self.app_logic.get_dashboard_data()

        player = dashboard_data["player"]
        stats = dashboard_data["stats"]
        self.active_quests = dashboard_data["active_quests"]
        recent_activity = dashboard_data["recent_activity"]

        if player is not None:
            self.player_label.setText(
                f"Player: {player.name} | Level: {player.level} | Gold: {player.gold} | EXP: {player.experience}"
            )
        else:
            self.player_label.setText("No player loaded.")

        self.stats_label.setText(
            f"Active Quests: {stats['active_quests']} | "
            f"Total Completed: {stats['total_completed']} | "
            f"Oldest Active Quest: {stats['oldest_active_quest']} | "
            f"Recent Activity Entries: {stats['recent_activity_count']}"
        )

        self.active_quest_list.clear()
        for quest in self.active_quests:
            self.active_quest_list.addItem(f"{quest.title} | {quest.difficulty.label} | {quest.length.label}")

        self.activity_list.clear()
        for entry in recent_activity:
            self.activity_list.addItem(f"{entry.quest_title} | +{entry.reward_gold} Gold | +{entry.reward_experience} EXP")

        if self.selected_quest is not None:
            refreshed_quest = self.app_logic.get_quest_by_id(self.selected_quest.id)

            if refreshed_quest is None or refreshed_quest.status.value != "Active":
                self.selected_quest = None
                self.detail_label.setText("Select an active quest to view details.")
            else:
                self.selected_quest = refreshed_quest
                self._update_detail_label()

    def select_quest(self, item) -> None:
        index = self.active_quest_list.row(item)
        self.selected_quest = self.active_quests[index]
        self._update_detail_label()

    def _update_detail_label(self) -> None:
        if self.selected_quest is None:
            self.detail_label.setText("Select an active quest to view details.")
            return

        reward_gold, reward_experience = self.app_logic.calculate_rewards(self.selected_quest)

        completed_at_text = (self.selected_quest.completed_at.strftime("%Y-%m-%d %H:%M:%S")
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
            f"Reward: {reward_gold} Gold, {reward_experience} EXP")

    def quick_complete_selected_quest(self) -> None:
        if self.selected_quest is None:
            QMessageBox.warning(self, "No Quest Selected", "Please select an active quest first.")
            return

        updated_quest, updated_player, reward_gold, reward_experience = self.app_logic.complete_quest(
            self.selected_quest.id
        )

        QMessageBox.information(
            self,
            "Quest Completed",
            f"Completed '{updated_quest.title}'\n"
            f"+{reward_gold} Gold\n"
            f"+{reward_experience} EXP\n"
            f"Player Gold: {updated_player.gold}\n"
            f"Player EXP: {updated_player.experience}"
        )

        self.selected_quest = None
        self.main_window.refresh_after_data_change()