from PySide6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Login menu
        login_menu = self.addMenu("Login")
        login_action = login_menu.addAction("Login to Space-track")
        login_action.triggered.connect(self.open_login_window)

        # Update menu
        update_menu = self.addMenu("Update")
        update_action = update_menu.addAction("Check for Updates")
        update_action.triggered.connect(self.open_update_window)

        # Help menu
        help_menu = self.addMenu("Help")
        help_action = help_menu.addAction("Help")
        help_action.triggered.connect(self.open_help_window)

    def open_help_window(self):
        pass

    def open_login_window(self):
        pass

    def open_update_window(self):
        pass