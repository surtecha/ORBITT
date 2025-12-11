from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                QLineEdit, QPushButton, QDateEdit, QMessageBox,
                                QProgressBar, QFormLayout, QGroupBox)
from PySide6.QtCore import Qt, QDate
from datetime import datetime
from backend.tle.spacetrack_fetcher import SpaceTrackTLEFetcher


class SpaceTrackTLEDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fetcher_thread = None
        self.tle_data = None
        
        self.setWindowTitle("Fetch TLE from Space-Track")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Fetch TLE Data from Space-Track")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        instructions = QLabel(
            "Enter NORAD ID(s) and date range to fetch TLE data.\n"
            "For multiple objects, separate IDs with commas (e.g., 25544, 25545, 25546)"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray;")
        layout.addWidget(instructions)
        
        form_group = QGroupBox("Parameters")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)
        
        self.norad_input = QLineEdit()
        self.norad_input.setPlaceholderText("e.g., 25544 or 25544, 25545, 25546")
        form_layout.addRow("NORAD ID(s):", self.norad_input)
        
        date_container = QHBoxLayout()
        date_container.setSpacing(15)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setMaximumDate(QDate.currentDate())
        date_container.addWidget(self.start_date)
        
        date_container.addWidget(QLabel("to"))
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setMaximumDate(QDate.currentDate())
        date_container.addWidget(self.end_date)
        
        form_layout.addRow("Date Range:", date_container)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(20)
        layout.addWidget(self.status_label)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(80)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.fetch_button = QPushButton("Fetch TLE")
        self.fetch_button.setMinimumWidth(80)
        self.fetch_button.setDefault(True)
        self.fetch_button.clicked.connect(self._on_fetch_clicked)
        button_layout.addWidget(self.fetch_button)
        
        layout.addLayout(button_layout)
        
    def _on_fetch_clicked(self):
        norad_text = self.norad_input.text().strip()
        if not norad_text:
            self._show_error("Please enter at least one NORAD ID")
            return
        
        try:
            norad_ids = [int(x.strip()) for x in norad_text.split(',')]
            if any(nid <= 0 for nid in norad_ids):
                raise ValueError()
        except ValueError:
            self._show_error("NORAD IDs must be positive integers separated by commas")
            return
        
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        
        if start > end:
            self._show_error("Start date must be before or equal to end date")
            return
        
        if end > datetime.now().date():
            self._show_error("End date cannot be in the future")
            return
        
        self._set_inputs_enabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Starting fetch...")
        self.status_label.setStyleSheet("font-weight: bold; color: #1976D2;")
        
        self.fetcher_thread = SpaceTrackTLEFetcher(norad_ids, start, end)
        self.fetcher_thread.progress_update.connect(self._on_progress_update)
        self.fetcher_thread.fetch_complete.connect(self._on_fetch_complete)
        self.fetcher_thread.start()
        
    def _on_progress_update(self, message):
        self.status_label.setText(message)
        
    def _on_fetch_complete(self, success, message, tle_data):
        self.progress_bar.setVisible(False)
        self._set_inputs_enabled(True)
        
        if success:
            self.tle_data = tle_data
            self.status_label.setText(message)
            self.status_label.setStyleSheet("font-weight: bold; color: #2E7D32;")
            
            QMessageBox.information(
                self,
                "Success",
                "TLE data fetched successfully!"
            )
            
            self.accept()
        else:
            self.status_label.setText(f"Error: {message}")
            self.status_label.setStyleSheet("font-weight: bold; color: #C62828;")
        
        if self.fetcher_thread:
            self.fetcher_thread.stop()
            self.fetcher_thread = None
    
    def _show_error(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("font-weight: bold; color: #C62828;")
    
    def _set_inputs_enabled(self, enabled):
        self.norad_input.setEnabled(enabled)
        self.start_date.setEnabled(enabled)
        self.end_date.setEnabled(enabled)
        self.fetch_button.setEnabled(enabled)
        self.cancel_button.setEnabled(enabled)
    
    def get_tle_data(self):
        return self.tle_data
    
    def closeEvent(self, event):
        if self.fetcher_thread and self.fetcher_thread.isRunning():
            self.fetcher_thread.stop()
        event.accept()
