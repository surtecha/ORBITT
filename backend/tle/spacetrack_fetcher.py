import requests
from PySide6.QtCore import QThread, Signal
from backend.utils.auth_config import AuthConfig


class SpaceTrackTLEFetcher(QThread):
    
    progress_update = Signal(str)
    fetch_complete = Signal(bool, str, str)

    def __init__(self, norad_ids, start_date, end_date):
        super().__init__()
        self.norad_ids = norad_ids
        self.start_date = start_date
        self.end_date = end_date
        self.auth_config = AuthConfig()
        self.session = None

    def run(self):
        try:
            self.progress_update.emit("Authenticating with Space-Track...")
            if not self._authenticate():
                self.fetch_complete.emit(False, "Authentication failed", "")
                return

            self.progress_update.emit(f"Fetching TLE data for {len(self.norad_ids)} object(s)...")
            tle_data = self._fetch_tle_data()
            
            if tle_data:
                self.progress_update.emit("TLE data fetched successfully")
                self.fetch_complete.emit(True, "Success", tle_data)
            else:
                self.fetch_complete.emit(False, "No TLE data found for the specified parameters", "")

        except Exception as e:
            self.fetch_complete.emit(False, f"Error: {str(e)}", "")
        finally:
            if self.session:
                self.session.close()

    def _authenticate(self):
        email, password = self.auth_config.get_credentials()
        if not email or not password:
            return False

        self.session = requests.Session()
        login_url = "https://www.space-track.org/ajaxauth/login"
        login_data = {
            'identity': email,
            'password': password
        }

        try:
            response = self.session.post(login_url, data=login_data, timeout=10)
            return response.status_code == 200
        except:
            return False

    def _fetch_tle_data(self):
        start_str = self.start_date.strftime('%Y-%m-%d')
        end_str = self.end_date.strftime('%Y-%m-%d')

        norad_ids_str = ','.join(map(str, self.norad_ids))
        
        url = (f"https://www.space-track.org/basicspacedata/query/class/gp_history/"
               f"NORAD_CAT_ID/{norad_ids_str}/"
               f"CREATION_DATE/{start_str}--{end_str}/"
               f"orderby/EPOCH/format/tle/")

        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200 and response.text.strip():
                return response.text
            return None
        except Exception as e:
            raise Exception(f"Failed to fetch TLE data: {str(e)}")

    def stop(self):
        if self.session:
            self.session.close()
        self.quit()
        self.wait()
