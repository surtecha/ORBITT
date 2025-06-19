from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QMessageBox, QProgressBar)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from config.auth_config import AuthConfig
from utils.spacetrack_auth import SpaceTrackAuth


class LoginWindow(QDialog):
    login_success = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_config = AuthConfig()
        self.auth_thread = None
        self.setup_ui()
        self.load_saved_credentials()

    def setup_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(500, 300)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title_label = QLabel("Space-Track Authentication")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        email_layout = QVBoxLayout()
        email_layout.setSpacing(8)
        email_label = QLabel("Email:")
        email_label_font = QFont()
        email_label_font.setBold(True)
        email_label.setFont(email_label_font)
        self.email_input = QLineEdit()
        self.email_input.setMinimumHeight(35)
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        password_layout = QVBoxLayout()
        password_layout.setSpacing(8)
        password_label = QLabel("Password:")
        password_label_font = QFont()
        password_label_font.setBold(True)
        password_label.setFont(password_label_font)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        self.login_button = QPushButton("Login")
        self.cancel_button = QPushButton("Cancel")

        self.login_button.setMinimumWidth(80)
        self.cancel_button.setMinimumWidth(80)

        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.attempt_login)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.login_button)
        layout.addLayout(button_layout)

        self.password_input.returnPressed.connect(self.attempt_login)
        self.email_input.returnPressed.connect(self.attempt_login)

    def load_saved_credentials(self):
        email, password = self.auth_config.get_credentials()
        if email:
            self.email_input.setText(email)
        if password:
            self.password_input.setText(password)

    def attempt_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Invalid Input", "Please enter both email and password.")
            return

        self.set_loading_state(True)

        self.auth_thread = SpaceTrackAuth(email, password)
        self.auth_thread.login_result.connect(self.handle_login_result)
        self.auth_thread.start()

    def handle_login_result(self, success, message):
        self.set_loading_state(False)

        if success:
            self.auth_config.save_credentials(self.email_input.text().strip(),
                                              self.password_input.text())
            QMessageBox.information(self, "Success", "Login successful!")
            self.login_success.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", f"Login failed: {message}")

        if self.auth_thread:
            self.auth_thread.stop()
            self.auth_thread = None

    def set_loading_state(self, loading):
        self.login_button.setEnabled(not loading)
        self.email_input.setEnabled(not loading)
        self.password_input.setEnabled(not loading)
        self.progress_bar.setVisible(loading)

        if loading:
            self.progress_bar.setRange(0, 0)
        else:
            self.progress_bar.setRange(0, 100)

    def closeEvent(self, event):
        if self.auth_thread:
            self.auth_thread.stop()
        event.accept()