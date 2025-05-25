from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QProgressBar, QFileDialog,
                             QMessageBox, QGroupBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings
import os
from utils.tle_extractor import TLEExtractor
from styles.stylesheet import get_button_style, get_widget_style

class ExtractionWorker(QThread):
    progress_updated = pyqtSignal(str)
    extraction_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, input_files, output_dir):
        super().__init__()
        self.input_files = input_files
        self.output_dir = output_dir
        self.extractor = TLEExtractor()

    def run(self):
        try:
            self.progress_updated.emit("Starting extraction process...")
            results = self.extractor.process_tle_files(
                self.input_files,
                self.output_dir,
                progress_callback=self.progress_updated.emit
            )
            self.extraction_completed.emit(results)
        except Exception as e:
            self.error_occurred.emit(f"Extraction failed: {str(e)}")


class Extractor(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.output_directory = ""
        self.settings = QSettings('ORBITT', 'TLEExtractor')
        self.extraction_worker = None
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        title_label = QLabel("TLE Data Extractor")
        title_label.setObjectName("extractorTitleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        input_group = QGroupBox("Input Files")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)

        file_selection_layout = QHBoxLayout()
        file_selection_layout.setSpacing(10)
        self.select_files_btn = QPushButton("Select TLE Files...")
        self.select_files_btn.setStyleSheet(get_button_style('primary'))
        self.select_files_btn.clicked.connect(self.select_files)

        self.clear_files_btn = QPushButton("Clear Selection")
        self.clear_files_btn.setStyleSheet(get_button_style('secondary'))
        self.clear_files_btn.clicked.connect(self.clear_files)
        self.clear_files_btn.setEnabled(False)

        file_selection_layout.addWidget(self.select_files_btn)
        file_selection_layout.addWidget(self.clear_files_btn)
        file_selection_layout.addStretch(1)
        input_layout.addLayout(file_selection_layout)

        self.files_display = QTextEdit()
        self.files_display.setFixedHeight(100)
        self.files_display.setReadOnly(True)
        self.files_display.setPlaceholderText("No files selected.")
        input_layout.addWidget(self.files_display)
        layout.addWidget(input_group)

        output_group = QGroupBox("Output Directory")
        output_layout = QVBoxLayout(output_group)
        output_layout.setSpacing(10)

        self.select_output_btn = QPushButton("Select Output Directory...")
        self.select_output_btn.setStyleSheet(get_button_style('secondary'))
        self.select_output_btn.clicked.connect(self.select_output_directory)
        
        output_button_layout = QHBoxLayout()
        output_button_layout.addWidget(self.select_output_btn)
        output_button_layout.addStretch(1)
        output_layout.addLayout(output_button_layout)

        self.output_display = QLabel("No output directory selected.")
        self.output_display.setStyleSheet(get_widget_style('labeled_output'))
        self.output_display.setWordWrap(True)
        output_layout.addWidget(self.output_display)
        layout.addWidget(output_group)

        extraction_group = QGroupBox("Extraction Process")
        extraction_layout = QVBoxLayout(extraction_group)
        extraction_layout.setSpacing(10)

        self.extract_btn = QPushButton("Start Extraction")
        self.extract_btn.setStyleSheet(get_button_style('success'))
        self.extract_btn.clicked.connect(self.start_extraction)
        self.extract_btn.setEnabled(False)
        extraction_layout.addWidget(self.extract_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        extraction_layout.addWidget(self.progress_bar)

        self.log_display = QTextEdit()
        self.log_display.setFixedHeight(150)
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Extraction logs will appear here...")
        extraction_layout.addWidget(self.log_display)
        layout.addWidget(extraction_group)

        layout.addStretch(1)


    def select_files(self):
        last_dir = self.settings.value("last_tle_dir", os.path.expanduser("~"))
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select TLE Files", last_dir, "Text Files (*.txt);;All Files (*)"
        )
        if files:
            self.selected_files = files
            self.update_files_display()
            self.clear_files_btn.setEnabled(True)
            self.check_extraction_ready()
            self.settings.setValue("last_tle_dir", os.path.dirname(files[0]))


    def clear_files(self):
        self.selected_files = []
        self.update_files_display()
        self.clear_files_btn.setEnabled(False)
        self.check_extraction_ready()

    def update_files_display(self):
        if self.selected_files:
            if len(self.selected_files) == 1:
                self.files_display.setText(f"Selected file: {os.path.basename(self.selected_files[0])}")
            else:
                self.files_display.setText(f"Selected {len(self.selected_files)} files:\n" +
                                           "\n".join([f"- {os.path.basename(f)}" for f in self.selected_files]))
        else:
            self.files_display.setPlaceholderText("No files selected.")
            self.files_display.clear()


    def select_output_directory(self):
        last_dir = self.settings.value("output_directory_parent", os.path.expanduser("~"))
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", last_dir)
        if directory:
            self.output_directory = os.path.join(directory, "tle-local-db")
            self.output_display.setText(f"{self.output_directory}")
            self.settings.setValue("output_directory_parent", directory)
            self.save_settings()
            self.check_extraction_ready()


    def check_extraction_ready(self):
        ready = bool(self.selected_files and self.output_directory)
        self.extract_btn.setEnabled(ready)

    def start_extraction(self):
        if not self.selected_files or not self.output_directory:
            QMessageBox.warning(self, "Input Missing", "Please select input TLE files and an output directory.")
            return

        self.extract_btn.setEnabled(False)
        self.select_files_btn.setEnabled(False)
        self.clear_files_btn.setEnabled(False)
        self.select_output_btn.setEnabled(False)

        self.progress_bar.setRange(0,0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.log_display.clear()
        self.update_log_progress("Starting TLE data extraction...")

        self.extraction_worker = ExtractionWorker(self.selected_files, self.output_directory)
        self.extraction_worker.progress_updated.connect(self.update_log_progress)
        self.extraction_worker.extraction_completed.connect(self.extraction_finished)
        self.extraction_worker.error_occurred.connect(self.extraction_error)
        self.extraction_worker.finished.connect(self.on_worker_finished)
        self.extraction_worker.start()

    def on_worker_finished(self):
        self.extract_btn.setEnabled(True)
        self.select_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(bool(self.selected_files))
        self.select_output_btn.setEnabled(True)
        self.check_extraction_ready()

    def update_log_progress(self, message):
        self.log_display.append(message)
        self.log_display.ensureCursorVisible()

    def extraction_finished(self, results):
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(100)
        
        summary = (
            f"\n--- Extraction Complete ---\n"
            f"Files processed: {results.get('files_processed', 0)}\n"
            f"Unique objects found: {results.get('objects_found', 0)}\n"
            f"Total TLEs processed: {results.get('tles_processed', 0)}\n"
            f"Output directory: {self.output_directory}"
        )
        self.log_display.append(summary)
        QMessageBox.information(self, "Extraction Complete", "TLE data extraction finished successfully.")

    def extraction_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.log_display.append(f"\n--- ERROR ---\n{error_message}")
        QMessageBox.critical(self, "Extraction Error", f"An error occurred: {error_message}")

    def save_settings(self):
        if self.output_directory:
            self.settings.setValue('output_directory', self.output_directory)

    def load_settings(self):
        saved_output = self.settings.value('output_directory', '')
        if saved_output and os.path.isdir(os.path.dirname(saved_output)):
            self.output_directory = saved_output
            self.output_display.setText(f"{self.output_directory}")
        else:
            self.output_directory = ""
            self.output_display.setText("No output directory selected.")
            self.settings.remove('output_directory')

        self.check_extraction_ready()