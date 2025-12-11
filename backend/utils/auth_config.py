from PySide6.QtCore import QSettings


class AuthConfig:
    
    def __init__(self):
        self.settings = QSettings("ORBITT", "SpaceTrack")
    
    def save_credentials(self, email, password):
        self.settings.setValue("email", email)
        self.settings.setValue("password", password)
    
    def get_credentials(self):
        email = self.settings.value("email", "")
        password = self.settings.value("password", "")
        return email, password
    
    def has_credentials(self):
        email, password = self.get_credentials()
        return bool(email and password)
    
    def clear_credentials(self):
        self.settings.remove("email")
        self.settings.remove("password")
