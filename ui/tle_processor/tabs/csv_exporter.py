from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QProgressBar, QFileDialog,
                             QMessageBox, QGroupBox, QSpacerItem, QSizePolicy,
                             QCheckBox)
from PyQt5.QtCore import Qt, QSettings
import os
from utils.csv_converter import CSVConversionWorker
from styles.stylesheet import get_button_style, get_widget_style

class CSVExporter(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.output_directory = ""
        self.settings = QSettings('ORBITT', 'CSVExporter')
        self.conversion_worker = None
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)
        
        title_label = QLabel("TLE to CSV Converter")
        title_label.setObjectName("extractorTitleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        input_group = QGroupBox("Input TLE Files")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)
        
        file_selection_layout = QHBoxLayout()
        file_selection_layout.setSpacing(10)
        
        self.select_files_btn = QPushButton("Select TLE Files...")
        self.select_files_btn.setStyleSheet(get_button_style('primary'))
        self.select_files_btn.clicked.connect(self.select_files)
        
        self.select_folder_btn = QPushButton("Select Folder...")
        self.select_folder_btn.setStyleSheet(get_button_style('primary'))
        self.select_folder_btn.clicked.connect(self.select_folder)
        
        self.clear_files_btn = QPushButton("Clear Selection")
        self.clear_files_btn.setStyleSheet(get_button_style('secondary'))
        self.clear_files_btn.clicked.connect(self.clear_files)
        self.clear_files_btn.setEnabled(False)
        
        file_selection_layout.addWidget(self.select_files_btn)
        file_selection_layout.addWidget(self.select_folder_btn)
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
        
        conversion_group = QGroupBox("Conversion Process")
        conversion_layout = QVBoxLayout(conversion_group)
        conversion_layout.setSpacing(10)
        
        self.convert_btn = QPushButton("Start Conversion")
        self.convert_btn.setStyleSheet(get_button_style('success'))
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        conversion_layout.addWidget(self.convert_btn)
        
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_label = QLabel("0%")
        self.progress_label.setMinimumWidth(40)
        self.progress_label.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        conversion_layout.addLayout(progress_layout)
        
        self.log_display = QTextEdit()
        self.log_display.setFixedHeight(150)
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Conversion logs will appear here...")
        conversion_layout.addWidget(self.log_display)
        layout.addWidget(conversion_group)
        
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
            self.check_conversion_ready()
            self.settings.setValue("last_tle_dir", os.path.dirname(files[0]))
    
    def select_folder(self):
        last_dir = self.settings.value("last_tle_dir", os.path.expanduser("~"))
        folder = QFileDialog.getExistingDirectory(self, "Select Folder with TLE Files", last_dir)
        if folder:
            txt_files = []
            for file in os.listdir(folder):
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(folder, file))
            
            if txt_files:
                self.selected_files = sorted(txt_files)
                self.update_files_display()
                self.clear_files_btn.setEnabled(True)
                self.check_conversion_ready()
                self.settings.setValue("last_tle_dir", folder)
            else:
                QMessageBox.information(self, "No TLE Files", "No .txt files found in the selected folder.")
    
    def clear_files(self):
        self.selected_files = []
        self.update_files_display()
        self.clear_files_btn.setEnabled(False)
        self.check_conversion_ready()
    
    def update_files_display(self):
        if self.selected_files:
            if len(self.selected_files) == 1:
                self.files_display.setText(f"Selected file: {os.path.basename(self.selected_files[0])}")
            else:
                file_list = "\n".join([f"- {os.path.basename(f)}" for f in self.selected_files[:10]])
                if len(self.selected_files) > 10:
                    file_list += f"\n... and {len(self.selected_files) - 10} more files"
                self.files_display.setText(f"Selected {len(self.selected_files)} files:\n{file_list}")
        else:
            self.files_display.setPlaceholderText("No files selected.")
            self.files_display.clear()
    
    def select_output_directory(self):
        last_dir = self.settings.value("output_directory_parent", os.path.expanduser("~"))
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", last_dir)
        if directory:
            self.output_directory = os.path.join(directory, "tle-csv-data")
            self.output_display.setText(f"{self.output_directory}")
            self.settings.setValue("output_directory_parent", directory)
            self.save_settings()
            self.check_conversion_ready()
    
    def check_conversion_ready(self):
        ready = bool(self.selected_files and self.output_directory)
        self.convert_btn.setEnabled(ready)
    
    def start_conversion(self):
        if not self.selected_files or not self.output_directory:
            QMessageBox.warning(self, "Input Missing", "Please select input TLE files and an output directory.")
            return
        
        self.convert_btn.setEnabled(False)
        self.select_files_btn.setEnabled(False)
        self.select_folder_btn.setEnabled(False)
        self.clear_files_btn.setEnabled(False)
        self.select_output_btn.setEnabled(False)
        
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_label.setText("0%")
        self.progress_label.setVisible(True)
        self.log_display.clear()
        self.update_log_progress("Starting TLE to CSV conversion...")
        
        self.conversion_worker = CSVConversionWorker(self.selected_files, self.output_directory)
        self.conversion_worker.progress_updated.connect(self.update_progress)
        self.conversion_worker.file_progress_updated.connect(self.update_log_progress)
        self.conversion_worker.conversion_completed.connect(self.conversion_finished)
        self.conversion_worker.error_occurred.connect(self.conversion_error)
        self.conversion_worker.finished.connect(self.on_worker_finished)
        self.conversion_worker.start()
    
    def on_worker_finished(self):
        self.convert_btn.setEnabled(True)
        self.select_files_btn.setEnabled(True)
        self.select_folder_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(bool(self.selected_files))
        self.select_output_btn.setEnabled(True)
        self.check_conversion_ready()
    
    def update_progress(self, percentage):
        self.progress_bar.setValue(percentage)
        self.progress_label.setText(f"{percentage}%")
    
    def update_log_progress(self, message):
        self.log_display.append(message)
        self.log_display.ensureCursorVisible()
    
    def conversion_finished(self, results):
        self.progress_bar.setValue(100)
        self.progress_label.setText("100%")
        
        summary = (
            f"\n--- Conversion Complete ---\n"
            f"Total files processed: {results.get('total_files', 0)}\n"
            f"Successful conversions: {results.get('successful_conversions', 0)}\n"
            f"Failed conversions: {results.get('failed_conversions', 0)}\n"
            f"Total records processed: {results.get('total_records', 0)}\n"
            f"Output directory: {self.output_directory}"
        )
        self.log_display.append(summary)
        QMessageBox.information(self, "Conversion Complete", "TLE to CSV conversion finished successfully.")
    
    def conversion_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.log_display.append(f"\n--- ERROR ---\n{error_message}")
        QMessageBox.critical(self, "Conversion Error", f"An error occurred: {error_message}")
    
    def save_settings(self):
        if self.output_directory:
            self.settings.setValue('csv_output_directory', self.output_directory)
    
    def load_settings(self):
        saved_output = self.settings.value('csv_output_directory', '')
        if saved_output and os.path.isdir(os.path.dirname(saved_output)):
            self.output_directory = saved_output
            self.output_display.setText(f"{self.output_directory}")
        else:
            self.output_directory = ""
            self.output_display.setText("No output directory selected.")
            self.settings.remove('csv_output_directory')
        
        self.check_conversion_ready()