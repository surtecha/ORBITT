import configparser
import os
from pathlib import Path
from cryptography.fernet import Fernet


class AuthConfig:
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / "config.ini"
        self.key_file = self.config_dir / ".key"
        self.config = configparser.ConfigParser()
        self.cipher = self._get_cipher()
        self.load_config()

    def _get_cipher(self):
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)

    def load_config(self):
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self.config.add_section('SPACETRACK')
            self.save_config()

    def save_config(self):
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def save_credentials(self, email, password):
        encrypted_password = self.cipher.encrypt(password.encode()).decode()
        self.config.set('SPACETRACK', 'email', email)
        self.config.set('SPACETRACK', 'password', encrypted_password)
        self.save_config()

    def get_credentials(self):
        if not self.config.has_section('SPACETRACK'):
            return None, None

        email = self.config.get('SPACETRACK', 'email', fallback='')
        encrypted_password = self.config.get('SPACETRACK', 'password', fallback='')

        if not email or not encrypted_password:
            return None, None

        try:
            password = self.cipher.decrypt(encrypted_password.encode()).decode()
            return email, password
        except:
            return None, None

    def clear_credentials(self):
        if self.config.has_section('SPACETRACK'):
            self.config.remove_section('SPACETRACK')
        self.config.add_section('SPACETRACK')
        self.save_config()

    def has_credentials(self):
        email, password = self.get_credentials()
        return email is not None and password is not None