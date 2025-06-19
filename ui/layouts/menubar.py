from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal, QTimer

from utils.login_util import LoginManager


class MenuBar(QMenuBar):
    login_status_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.login_manager = LoginManager(parent)

        self.login_menu = None
        self.login_action = None
        self.logout_action = None

        self.login_manager.login_status_changed.connect(self.on_login_status_changed)
        self.setup_menus()
        self.update_login_menu()

    def setup_menus(self):
        self.login_menu = self.addMenu("Login")
        self.login_action = self.login_menu.addAction("Login to Space-track")
        self.login_action.triggered.connect(self.login_manager.handle_login_click)

        self.logout_action = self.login_menu.addAction("Logout")
        self.logout_action.triggered.connect(self.login_manager.handle_logout_click)

        update_menu = self.addMenu("Update")
        update_action = update_menu.addAction("Check for Updates")
        update_action.triggered.connect(self.open_update_window)

        help_menu = self.addMenu("Help")
        help_action = help_menu.addAction("Help")
        help_action.triggered.connect(self.open_help_window)

    def update_login_menu(self):
        self.login_manager.update_menu_state(self.login_action, self.logout_action)

    def on_login_status_changed(self, is_logged_in):
        QTimer.singleShot(0, self.update_login_menu)
        self.login_status_changed.emit(is_logged_in)

    def open_help_window(self):
        pass

    def open_update_window(self):
        pass