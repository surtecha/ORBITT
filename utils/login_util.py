from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal

from config.auth_config import AuthConfig
from ui.dialogs.login_window import LoginWindow


class LoginManager(QObject):
    login_status_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.auth_config = AuthConfig()
        self.login_window = None

    def get_login_status(self):
        return self.auth_config.has_credentials()

    def get_current_user_email(self):
        email, _ = self.auth_config.get_credentials()
        return email

    def get_login_display_text(self):
        if self.get_login_status():
            email = self.get_current_user_email()
            return f"Logged in as: {email}"
        return "Login to Space-track"

    def should_show_logout(self):
        return self.get_login_status()

    def should_enable_login(self):
        return not self.get_login_status()

    def handle_login_click(self):
        if not self.get_login_status():
            self.open_login_window()

    def handle_logout_click(self):
        reply = QMessageBox.question(
            self.parent,
            "Logout",
            "Are you sure you want to logout from Space-track?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.auth_config.clear_credentials()
            self.login_status_changed.emit(False)
            QMessageBox.information(self.parent, "Logout", "Successfully logged out from Space-track.")

    def update_menu_state(self, login_action, logout_action):
        login_action.setText(self.get_login_display_text())
        login_action.setEnabled(self.should_enable_login())
        logout_action.setVisible(self.should_show_logout())

    def open_login_window(self):
        if self.login_window is None:
            self.login_window = LoginWindow(self.parent)
            self.login_window.login_success.connect(self.on_login_success)

        self.login_window.show()
        self.login_window.raise_()
        self.login_window.activateWindow()

    def on_login_success(self):
        if self.login_window:
            self.login_window.close()
            self.login_window = None
        self.login_status_changed.emit(True)