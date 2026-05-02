from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

from logic.app_logic import AppLogic


class ActivityLogPage(QWidget):
    def __init__(self, app_logic: AppLogic, main_window):
        super().__init__()

        self.app_logic = app_logic
        self.main_window = main_window

        layout = QVBoxLayout(self)

        self.title_label = QLabel("Activity Log")
        self.summary_label = QLabel("Recent completion history will appear here.")
        self.activity_list = QListWidget()
        # Add Widgets- activity list data populated on refresh()
        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.activity_list)

        self.refresh()

    def refresh(self) -> None:
        activity_entries = self.app_logic.get_recent_activity(limit=50)

        self.activity_list.clear()
 
        if not activity_entries:
            self.summary_label.setText("No recent activity yet.")
            return

        self.summary_label.setText(f"Showing {len(activity_entries)} recent activity entries.")
    # display for activity log info
        for entry in activity_entries:
            completed_text = entry.completed_at.strftime("%Y-%m-%d %H:%M")
            self.activity_list.addItem(
                f"{completed_text} | {entry.quest_title} | "
                f"+{entry.reward_gold} Gold | +{entry.reward_experience} EXP"
            )