import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from PySide6.QtCore import QThread, Signal
from config.auth_config import AuthConfig
from core.tle.tle_processor import read_tle_file, read_existing_tles
from core.tle.csv_convertor import calculate_all_parameters, save_to_csv, append_to_csv


class TLEFetcher(QThread):
    log_message = Signal(str)
    fetching_progress = Signal(int)
    extraction_progress = Signal(int)
    conversion_progress = Signal(int)
    metrics_updated = Signal(int, int)
    last_fetched_updated = Signal(str)
    finished = Signal()

    def __init__(self, start_date, output_folder, objects_folder):
        super().__init__()
        self.start_date = start_date
        self.output_folder = Path(output_folder)
        self.objects_folder = Path(objects_folder)
        self.txt_folder = self.objects_folder / "txt"
        self.csv_folder = self.objects_folder / "csv"
        self.auth_config = AuthConfig()
        self.session = None
        self.total_tles_processed = 0
        self.unique_norads = set()

    def run(self):
        try:
            self._setup_directories()
            self._authenticate()
            self._fetch_tle_data()
            self._process_downloaded_files()
            self._finalize_processing()
        except Exception as e:
            self.log_message.emit(f"❌ Error during fetching: {str(e)}")
        finally:
            if self.session:
                self.session.close()
            self.finished.emit()

    def _setup_directories(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.txt_folder.mkdir(parents=True, exist_ok=True)
        self.csv_folder.mkdir(parents=True, exist_ok=True)

    def _authenticate(self):
        email, password = self.auth_config.get_credentials()
        if not email or not password:
            raise Exception("No Space-Track credentials found")

        self.session = requests.Session()
        login_url = "https://www.space-track.org/ajaxauth/login"
        login_data = {
            'identity': email,
            'password': password
        }

        response = self.session.post(login_url, data=login_data)
        if response.status_code != 200:
            raise Exception("Failed to authenticate with Space-Track")

        self.log_message.emit("✅ Authenticated with Space-Track")

    def _fetch_tle_data(self):
        current_date = self.start_date
        today = datetime.now().date()
        total_days = (today - current_date).days
        processed_days = 0

        while current_date < today:
            next_date = current_date + timedelta(days=1)
            self._fetch_single_day(current_date, next_date)

            current_date = next_date
            processed_days += 1

            progress = int((processed_days / total_days) * 100) if total_days > 0 else 100
            self.fetching_progress.emit(progress)

            self.last_fetched_updated.emit(current_date.strftime('%Y-%m-%d'))

            time.sleep(15)

        self.fetching_progress.emit(100)

    def _fetch_single_day(self, start_date, end_date):
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        url = f"https://www.space-track.org/basicspacedata/query/class/gp_history/CREATION_DATE/{start_str}--{end_str}/orderby/NORAD_CAT_ID,EPOCH/format/tle/"

        self.log_message.emit(f"📡 Fetching TLEs for {start_str}")

        try:
            response = self.session.get(url)
            if response.status_code == 200 and response.text.strip():
                filename = f"tle_{start_str}.txt"
                filepath = self.output_folder / filename

                with open(filepath, 'w') as f:
                    f.write(response.text)

                self.log_message.emit(f"✅ Downloaded {filename}")
            else:
                self.log_message.emit(f"⚠️ No data for {start_str}")
        except Exception as e:
            self.log_message.emit(f"❌ Failed to fetch {start_str}: {str(e)}")

    def _process_downloaded_files(self):
        tle_files = list(self.output_folder.glob("tle_*.txt"))
        if not tle_files:
            self.log_message.emit("⚠️ No TLE files found to process")
            return

        self.log_message.emit("🔄 Starting object sorting...")
        self._extract_objects_from_files(tle_files)

        self.log_message.emit("📊 Starting CSV conversion...")
        self._convert_objects_to_csv()

    def _extract_objects_from_files(self, tle_files):
        total_files = len(tle_files)

        for file_index, filepath in enumerate(tle_files):
            self.log_message.emit(f"📂 Processing {filepath.name}")

            tle_data = read_tle_file(str(filepath))
            if not tle_data:
                self.log_message.emit(f"⚠️ No TLE data found in {filepath.name}")
                continue

            file_tles_count = sum(len(tles) for tles in tle_data.values())
            self.total_tles_processed += file_tles_count

            processed_norads = self._extract_tles_to_files(tle_data, filepath.name)
            self.unique_norads.update(processed_norads)

            progress = int(((file_index + 1) / total_files) * 100)
            self.extraction_progress.emit(progress)

            self.metrics_updated.emit(self.total_tles_processed, len(self.unique_norads))

    def _extract_tles_to_files(self, tle_data, source_filename):
        processed_norads = set()

        for norad_id, new_tles in tle_data.items():
            output_file = self.txt_folder / f"{norad_id}.txt"

            existing_tles = read_existing_tles(str(output_file)) if output_file.exists() else []
            all_tles = existing_tles + new_tles
            sorted_tles = sorted(all_tles, key=lambda x: x[0] if x[0] else 0)

            with open(output_file, 'w') as file:
                for _, line1, line2 in sorted_tles:
                    file.write(f"{line1}\n{line2}\n")

            processed_norads.add(norad_id)

        self.log_message.emit(f"🔄 Extracted {len(processed_norads)} NORAD objects from {source_filename}")
        return processed_norads

    def _convert_objects_to_csv(self):
        converted_count = 0
        total_norads = len(self.unique_norads)
        norad_list = list(self.unique_norads)

        for i, norad_id in enumerate(norad_list):
            if self._convert_single_norad_to_csv(norad_id):
                converted_count += 1

            if total_norads > 0:
                progress = int(((i + 1) / total_norads) * 100)
                self.conversion_progress.emit(progress)

        self.log_message.emit(f"📊 Converted {converted_count}/{total_norads} files to CSV")

    def _convert_single_norad_to_csv(self, norad_id):
        txt_file = self.txt_folder / f"{norad_id}.txt"
        csv_file = self.csv_folder / f"{norad_id}.csv"

        if not txt_file.exists():
            self.log_message.emit(f"  └─ {norad_id}: TXT file not found ❌")
            return False

        try:
            tle_data = read_tle_file(str(txt_file))
            if not tle_data or norad_id not in tle_data:
                self.log_message.emit(f"  └─ {norad_id}: No TLE data found ❌")
                return False

            csv_data = []
            for _, line1, line2 in tle_data[norad_id]:
                try:
                    params = calculate_all_parameters(line1, line2)
                    csv_data.append(params)
                except Exception as e:
                    self.log_message.emit(f"  └─ {norad_id}: Error processing TLE ❌")
                    continue

            if csv_data:
                if csv_file.exists():
                    append_to_csv(csv_data, str(csv_file))
                else:
                    save_to_csv(csv_data, str(csv_file))
                self.log_message.emit(f"  └─ {norad_id}: Converted to CSV ✅")
                return True
            else:
                self.log_message.emit(f"  └─ {norad_id}: No valid TLE data ❌")
                return False

        except Exception as e:
            self.log_message.emit(f"  └─ {norad_id}: Processing failed ❌")
            return False

    def _finalize_processing(self):
        self.extraction_progress.emit(100)
        self.conversion_progress.emit(100)
        self.log_message.emit("🎉 All fetching and processing completed")