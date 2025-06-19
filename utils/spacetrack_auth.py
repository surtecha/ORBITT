import requests
from PySide6.QtCore import QThread, Signal


class SpaceTrackAuth(QThread):
    login_result = Signal(bool, str)

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password
        self.session = requests.Session()

    def run(self):
        try:
            login_url = "https://www.space-track.org/ajaxauth/login"
            login_data = {
                'identity': self.email,
                'password': self.password
            }

            response = self.session.post(login_url, data=login_data, timeout=10)

            if response.status_code == 200:
                test_url = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/limit/1/format/json"
                test_response = self.session.get(test_url, timeout=10)

                if test_response.status_code == 200:
                    try:
                        data = test_response.json()
                        if isinstance(data, list) and len(data) > 0:
                            self.login_result.emit(True, "Login successful")
                        else:
                            self.login_result.emit(False, "Authentication failed")
                    except:
                        self.login_result.emit(False, "Invalid response format")
                else:
                    self.login_result.emit(False, "Authentication failed")
            else:
                self.login_result.emit(False, "Login request failed")

        except requests.exceptions.Timeout:
            self.login_result.emit(False, "Connection timeout")
        except requests.exceptions.RequestException as e:
            self.login_result.emit(False, f"Network error: {str(e)}")
        except Exception as e:
            self.login_result.emit(False, f"Unexpected error: {str(e)}")

    def stop(self):
        self.session.close()
        self.quit()
        self.wait()


def validate_spacetrack_credentials(email, password):
    if not email or not password:
        return False, "Email and password are required"
    if '@' not in email:
        return False, "Please enter a valid email address"
    return True, ""


def create_spacetrack_session(email, password):
    session = requests.Session()
    try:
        login_url = "https://www.space-track.org/ajaxauth/login"
        login_data = {
            'identity': email,
            'password': password
        }

        response = session.post(login_url, data=login_data, timeout=10)

        if response.status_code == 200:
            return session, True, "Session created successfully"
        else:
            session.close()
            return None, False, "Failed to create session"

    except Exception as e:
        session.close()
        return None, False, f"Error creating session: {str(e)}"