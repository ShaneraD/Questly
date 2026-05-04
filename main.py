import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from storage.database import DatabaseManager
from logic.app_logic import AppLogic
from pathlib import Path

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    base_dir = Path(__file__).resolve().parent
    icon_path = base_dir / "assets" / "questly.ico"
    app.setWindowIcon(QIcon(str(icon_path)))

    db = DatabaseManager()
    db.initialize_database()

    logic = AppLogic(db)

    window = MainWindow(logic)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()