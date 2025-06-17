from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout
from ui.components.input_folder_selector import InputFolderSelector
from ui.components.progress_bar import ProgressBar
from ui.components.log_viewer import LogViewer
from core.tle.bulk_extractor_worker import BulkExtractorWorker
from config.data_config import DataConfig


class BulkExtractorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.config_manager = DataConfig()

        self.input_folder_selector = None
        self.run_button = None
        self.extraction_progress = None
        self.conversion_progress = None
        self.log_viewer = None
        self.tles_processed_label = None
        self.unique_objects_label = None

        self.total_tles = 0
        self.unique_objects = 0

        self.setup_ui()
        self.create_sidebar_widgets()

    def setup_ui(self):
        layout = QVBoxLayout()
        progress_layout = QVBoxLayout()

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
        self.input_folder_selector = InputFolderSelector("Select input folder")
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.start_processing)
        self.tles_processed_label = QLabel("Number of TLEs processed: 0")
        self.unique_objects_label = QLabel("Number of unique objects: 0")

    def get_sidebar_widgets(self):
        primary = [
            QLabel("Input Path"),
            self.input_folder_selector,
            self.run_button
        ]
        secondary = [
            self.tles_processed_label,
            self.unique_objects_label
        ]
        return primary, secondary

    def start_processing(self):
        selected_files = self.input_folder_selector.get_selected_files()
        input_folder = self.input_folder_selector.get_folder_path()
        objects_folder = self.config_manager.get_objects_directory()

        if not selected_files:
            self.log_viewer.add_log("⚠️ No files selected for processing")
            return
        if not input_folder:
            self.log_viewer.add_log("⚠️ No input folder selected")
            return
        if not objects_folder:
            self.log_viewer.add_log("⚠️ No data directory configured")
            return

        if self.worker and self.worker.isRunning():
            self.log_viewer.add_log("⚠️ Processing already in progress")
            return

        self.worker = BulkExtractorWorker(selected_files, input_folder, objects_folder)
        self._connect_worker_signals()

        self.run_button.setEnabled(False)
        self.extraction_progress.setValue(0)
        self.conversion_progress.setValue(0)
        self.log_viewer.clear_log()

        self.worker.start()
        self.log_viewer.add_log("🚀 Starting bulk extraction process...")

    def _connect_worker_signals(self):
        self.worker.extraction_progress.connect(self.extraction_progress.setValue)
        self.worker.conversion_progress.connect(self.conversion_progress.setValue)
        self.worker.log_message.connect(self.log_viewer.add_log)
        self.worker.metrics_updated.connect(self.update_metrics)
        self.worker.finished.connect(self.on_processing_finished)

    def update_metrics(self, total_tles, unique_objects):
        self.total_tles = total_tles
        self.unique_objects = unique_objects
        self.tles_processed_label.setText(f"Number of TLEs processed: {total_tles}")
        self.unique_objects_label.setText(f"Number of unique objects: {unique_objects}")

    def on_processing_finished(self):
        self.run_button.setEnabled(True)
        self.log_viewer.add_log("🏁 Processing completed")

        if self.worker:
            self.worker.deleteLater()
            self.worker = None


_tab_instance = None

def get_tab_widget():
    global _tab_instance
    if _tab_instance is None:
        _tab_instance = BulkExtractorTab()
    return _tab_instance

def get_sidebar_widgets():
    return get_tab_widget().get_sidebar_widgets()