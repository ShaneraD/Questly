Questly Readme Documentation
======================================

Questly is a gamified task and habit tracking application built with Python, PySide6, and SQLite.
The program allows users to create quests, complete one-time or repeatable quests, earn gold and
experience, track activity history, and manage progress through a graphical user interface.


Files
-----
- main.py - application entry point
- models/ - data models and enums
- storage/ - SQLite database logic
- logic/ - application workflow and reward logic
- ui/ - interface files, pages, dialogs, and main window
- data/ - SQLite database file created during runtime


Requirements
------------
- Python 3.10 or newer
- PySide6 installed if running from source
- Windows desktop environment recommended for current testing


Installation / Running from Source
----------------------------------
1. Download or copy the Questly project folder to your computer.

2. Open a terminal or command prompt in the project folder.

3. Install dependencies:
pip install PySide6

4. Run the application:
python main.py

5. The database file will be created automatically on first run if it does not already exist.


Running as a Packaged Executable
--------------------------------
1. If Questly has been packaged as a standalone executable, no separate Python or PySide6 nstallation is required for the end user.

2. Open the distributed Questly executable or application folder.

3. Launch the application from the provided executable file.


Usage
-----
1. Open Questly.
2. Use the Dashboard to view player information, active quests, and recent activity.
3. Use the Quests page to create, edit, complete, archive, or delete quests.
4. Use the Rewards page to review progression and reward scaling.
5. Use the Activity Log to review recent completed quest history.


Considerations
--------------
- One-time quests move out of active views when completed.
- Repeatable quests remain active and increase their completion count.
- Current settings and some support features are starter implementations and may be expanded in later versions.


Contact
-------
SDEV 265 Purple Group Development Team
