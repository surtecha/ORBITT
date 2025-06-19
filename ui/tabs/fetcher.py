from datetime import datetime
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout
from ui.components.progress_bar import ProgressBar
from ui.components.log_viewer import LogViewer
from core.tle.tle_fetcher import TLEFetcher
from config.data_config import DataConfig
from config.auth_config import AuthConfig


class FetcherTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.config_manager = DataConfig()
        self.auth_config = AuthConfig()

        self.fetch_button = None
        self.fetching_progress = None
        self.extraction_progress = None
        self.conversion_progress = None
        self.log_viewer = None
        self.last_fetched_label = None
        self.tles_processed_label = None
        self.unique_objects_label = None

        self.total_tles = 0
        self.unique_objects = 0

        self.setup_ui()
        self.create_sidebar_widgets()

    def setup_ui(self):
        layout = QVBoxLayout()
        progress_layout = QVBoxLayout()

        progress_layout.addWidget(QLabel("Fetching"))
        self.fetching_progress = ProgressBar()
        progress_layout.addWidget(self.fetching_progress)

        progress_layout.addWidget(QLabel("Object Sorting"))
        self.extraction_progress = ProgressBar()
        progress_layout.addWidget(self.extraction_progress)

        progress_layout.addWidget(QLabel("Converting to CSV"))
        self.conversion_progress = ProgressBar()
        progress_layout.addWidget(self.conversion_progress)

        layout.addLayout(progress_layout)

        self.log_viewer = LogViewer()
        layout.addWidget(self.log_viewer, 1)

        self.setLayout(layout)

    def create_sidebar_widgets(self):
        last_fetched = self.config_manager.get_last_fetched_date()
        self.last_fetched_label = QLabel(f"Last fetched: {last_fetched}")
        self.fetch_button = QPushButton("Fetch")
        self.fetch_button.clicked.connect(self.start_fetching)
        self.tles_processed_label = QLabel("Number of TLEs processed: 0")
        self.unique_objects_label = QLabel("Number of unique objects: 0")

    def get_sidebar_widgets(self):
        primary = [
            self.last_fetched_label,
            self.fetch_button
        ]
        secondary = [
            self.tles_processed_label,
            self.unique_objects_label
        ]
        return primary, secondary

    def start_fetching(self):
        if not self.auth_config.has_credentials():
            self.log_viewer.add_log("⚠️ No Space-Track credentials configured")
            return

        raw_folder = self.config_manager.get_raw_directory()
        objects_folder = self.config_manager.get_objects_directory()

        if not raw_folder:
            self.log_viewer.add_log("⚠️ No data directory configured")
            return

        if self.worker and self.worker.isRunning():
            self.log_viewer.add_log("⚠️ Fetching already in progress")
            return

        last_fetched_str = self.config_manager.get_last_fetched_date()
        try:
            start_date = datetime.strptime(last_fetched_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime(2025, 1, 1).date()

        self.worker = TLEFetcher(start_date, raw_folder, objects_folder)
        self._connect_worker_signals()

        self.fetch_button.setEnabled(False)
        self.fetching_progress.setValue(0)
        self.extraction_progress.setValue(0)
        self.conversion_progress.setValue(0)
        self.log_viewer.clear_log()

        self.worker.start()
        self.log_viewer.add_log("🚀 Starting TLE fetching process...")

    def _connect_worker_signals(self):
        self.worker.fetching_progress.connect(self.fetching_progress.setValue)
        self.worker.extraction_progress.connect(self.extraction_progress.setValue)
        self.worker.conversion_progress.connect(self.conversion_progress.setValue)
        self.worker.log_message.connect(self.log_viewer.add_log)
        self.worker.metrics_updated.connect(self.update_metrics)
        self.worker.last_fetched_updated.connect(self.update_last_fetched)
        self.worker.finished.connect(self.on_fetching_finished)

    def update_metrics(self, total_tles, unique_objects):
        self.total_tles = total_tles
        self.unique_objects = unique_objects
        self.tles_processed_label.setText(f"Number of TLEs processed: {total_tles}")
        self.unique_objects_label.setText(f"Number of unique objects: {unique_objects}")

    def update_last_fetched(self, date_str):
        self.config_manager.set_last_fetched_date(date_str)
        self.last_fetched_label.setText(f"Last fetched: {date_str}")

    def on_fetching_finished(self):
        self.fetch_button.setEnabled(True)
        self.log_viewer.add_log("🏁 Fetching completed")

        if self.worker:
            self.worker.deleteLater()
            self.worker = None


_tab_instance = None

def get_tab_widget():
    global _tab_instance
    if _tab_instance is None:
        _tab_instance = FetcherTab()
    return _tab_instance

def get_sidebar_widgets():
    return get_tab_widget().get_sidebar_widgets()