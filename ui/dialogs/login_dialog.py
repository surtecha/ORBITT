from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal
from backend.utils.spacetrack import SpaceTrackAuth, validate_spacetrack_credentials
from backend.utils.auth_config import AuthConfig


class LoginDialog(QDialog):
    
    login_success = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_config = AuthConfig()
        self.auth_thread = None
        
        self.setWindowTitle("Login to Space-Track")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel("Space-Track Login")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        instructions = QLabel(
            "Enter your Space-Track credentials.\n"
            "Don't have an account? Register at space-track.org"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray;")
        layout.addWidget(instructions)
        
        email_label = QLabel("Email:")
        layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.email@example.com")
        layout.addWidget(self.email_input)
        
        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password")
        layout.addWidget(self.password_input)
        
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.login_button = QPushButton("Login")
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self._on_login_clicked)
        button_layout.addWidget(self.login_button)
        
        layout.addLayout(button_layout)
        
        self.password_input.returnPressed.connect(self._on_login_clicked)
        
    def _on_login_clicked(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        valid, message = validate_spacetrack_credentials(email, password)
        if not valid:
            self.status_label.setText(message)
            self.status_label.setStyleSheet("font-weight: bold; color: #C62828;")
            return
        
        self._set_inputs_enabled(False)
        self.status_label.setText("Authenticating...")
        self.status_label.setStyleSheet("font-weight: bold; color: #1976D2;")
        
        self.auth_thread = SpaceTrackAuth(email, password)
        self.auth_thread.login_result.connect(self._on_login_result)
        self.auth_thread.start()
        
    def _on_login_result(self, success, message):
        self._set_inputs_enabled(True)
        
        if success:
            email = self.email_input.text().strip()
            password = self.password_input.text()
            self.auth_config.save_credentials(email, password)
            
            QMessageBox.information(
                self,
                "Login Successful",
                "Successfully logged in to Space-Track!"
            )
            
            self.login_success.emit()
            self.accept()
        else:
            self.status_label.setText(f"Login failed: {message}")
            self.status_label.setStyleSheet("font-weight: bold; color: #C62828;")
        
        if self.auth_thread:
            self.auth_thread.stop()
            self.auth_thread = None
    
    def _set_inputs_enabled(self, enabled):
        self.email_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)
        self.login_button.setEnabled(enabled)
        self.cancel_button.setEnabled(enabled)
    
    def closeEvent(self, event):
        if self.auth_thread and self.auth_thread.isRunning():
            self.auth_thread.stop()
        event.accept()
