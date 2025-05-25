from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QProgressBar, QFileDialog, 
                             QMessageBox, QFrame, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QPixmap
import os
from utils.tle_extractor import TLEExtractor

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
            self.error_occurred.emit(str(e))

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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("TLE Data Extractor")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        input_group = QGroupBox("Input Files")
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin: 10px 0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        input_layout = QVBoxLayout(input_group)
        
        file_selection_layout = QHBoxLayout()
        self.select_files_btn = QPushButton("Select TLE Files")
        self.select_files_btn.setFixedHeight(35)
        self.select_files_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        self.select_files_btn.clicked.connect(self.select_files)
        
        self.clear_files_btn = QPushButton("Clear Selection")
        self.clear_files_btn.setFixedHeight(35)
        self.clear_files_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.clear_files_btn.clicked.connect(self.clear_files)
        self.clear_files_btn.setEnabled(False)
        
        file_selection_layout.addWidget(self.select_files_btn)
        file_selection_layout.addWidget(self.clear_files_btn)
        file_selection_layout.addStretch()
        
        input_layout.addLayout(file_selection_layout)
        
        self.files_display = QTextEdit()
        self.files_display.setFixedHeight(120)
        self.files_display.setReadOnly(True)
        self.files_display.setPlaceholderText("No files selected")
        self.files_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        input_layout.addWidget(self.files_display)
        
        layout.addWidget(input_group)
        
        output_group = QGroupBox("Output Directory")
        output_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin: 10px 0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        output_layout = QVBoxLayout(output_group)
        
        output_selection_layout = QHBoxLayout()
        self.select_output_btn = QPushButton("Select Output Directory")
        self.select_output_btn.setFixedHeight(35)
        self.select_output_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.select_output_btn.clicked.connect(self.select_output_directory)
        
        output_selection_layout.addWidget(self.select_output_btn)
        output_selection_layout.addStretch()
        
        output_layout.addLayout(output_selection_layout)
        
        self.output_display = QLabel("No output directory selected")
        self.output_display.setStyleSheet("""
            QLabel {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
                font-family: 'Consolas', monospace;
                font-size: 10px;
                min-height: 20px;
            }
        """)
        self.output_display.setWordWrap(True)
        output_layout.addWidget(self.output_display)
        
        layout.addWidget(output_group)
        
        extraction_group = QGroupBox("Extraction Process")
        extraction_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin: 10px 0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        extraction_layout = QVBoxLayout(extraction_group)
        
        self.extract_btn = QPushButton("Start Extraction")
        self.extract_btn.setFixedHeight(45)
        self.extract_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
            QPushButton:pressed {
                background-color: #d39e00;
            }
            QPushButton:disabled {
                background-color: #f8f9fa;
                color: #6c757d;
            }
        """)
        self.extract_btn.clicked.connect(self.start_extraction)
        self.extract_btn.setEnabled(False)
        extraction_layout.addWidget(self.extract_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 3px;
            }
        """)
        extraction_layout.addWidget(self.progress_bar)
        
        self.log_display = QTextEdit()
        self.log_display.setFixedHeight(200)
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Extraction logs will appear here...")
        self.log_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        extraction_layout.addWidget(self.log_display)
        
        layout.addWidget(extraction_group)
        
        layout.addStretch()
        
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select TLE Files",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if files:
            self.selected_files = files
            self.update_files_display()
            self.clear_files_btn.setEnabled(True)
            self.check_extraction_ready()
            
    def clear_files(self):
        self.selected_files = []
        self.update_files_display()
        self.clear_files_btn.setEnabled(False)
        self.check_extraction_ready()
        
    def update_files_display(self):
        if self.selected_files:
            file_list = "\n".join([os.path.basename(f) for f in self.selected_files])
            self.files_display.setText(f"Selected {len(self.selected_files)} files:\n{file_list}")
        else:
            self.files_display.clear()
            
    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory"
        )
        
        if directory:
            self.output_directory = os.path.join(directory, "tle-local-db")
            self.output_display.setText(f"Output: {self.output_directory}")
            self.save_settings()
            self.check_extraction_ready()
            
    def check_extraction_ready(self):
        ready = bool(self.selected_files and self.output_directory)
        self.extract_btn.setEnabled(ready)
        
    def start_extraction(self):
        if not self.selected_files or not self.output_directory:
            QMessageBox.warning(self, "Warning", "Please select input files and output directory.")
            return
            
        self.extract_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.log_display.clear()
        
        self.extraction_worker = ExtractionWorker(self.selected_files, self.output_directory)
        self.extraction_worker.progress_updated.connect(self.update_log)
        self.extraction_worker.extraction_completed.connect(self.extraction_finished)
        self.extraction_worker.error_occurred.connect(self.extraction_error)
        self.extraction_worker.start()
        
    def update_log(self, message):
        self.log_display.append(message)
        self.log_display.ensureCursorVisible()
        
    def extraction_finished(self, results):
        self.progress_bar.setVisible(False)
        self.extract_btn.setEnabled(True)
        
        summary = f"""
Extraction completed successfully!

Files processed: {results.get('files_processed', 0)}
Unique objects found: {results.get('objects_found', 0)}
Total TLEs processed: {results.get('tles_processed', 0)}
Output directory: {self.output_directory}
        """
        
        self.log_display.append(summary)
        
        QMessageBox.information(
            self, 
            "Extraction Complete", 
            f"Successfully processed {results.get('files_processed', 0)} files.\n"
            f"Found {results.get('objects_found', 0)} unique objects.\n"
            f"Processed {results.get('tles_processed', 0)} TLEs."
        )
        
    def extraction_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.extract_btn.setEnabled(True)
        
        self.log_display.append(f"Error: {error_message}")
        
        QMessageBox.critical(
            self, 
            "Extraction Error", 
            f"An error occurred during extraction:\n{error_message}"
        )
        
    def save_settings(self):
        self.settings.setValue('output_directory', self.output_directory)
        
    def load_settings(self):
        saved_output = self.settings.value('output_directory', '')
        if saved_output:
            self.output_directory = saved_output
            self.output_display.setText(f"Output: {self.output_directory}")
            self.check_extraction_ready()