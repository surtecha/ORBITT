from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

class Extractor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        title_label = QLabel("Data Extraction Tool")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: black; background: transparent; border: none; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Extract and export TLE data in various formats")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #666666; background: transparent; border: none; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
        options_container = QWidget()
        options_container.setStyleSheet("background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px;")
        options_layout = QVBoxLayout(options_container)
        options_layout.setSpacing(20)
        
        format_row = QHBoxLayout()
        format_label = QLabel("Export Format:")
        format_label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
        format_row.addWidget(format_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "JSON", "XML", "TXT"])
        self.format_combo.setFixedHeight(35)
        self.format_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 5px 10px;
                color: black;
                font-size: 10px;
            }
            QComboBox:hover {
                border: 1px solid #0078d4;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid black;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #c0c0c0;
                selection-background-color: #e3f2fd;
            }
        """)
        format_row.addWidget(self.format_combo)
        format_row.addStretch()
        options_layout.addLayout(format_row)
        
        records_row = QHBoxLayout()
        records_label = QLabel("Max Records:")
        records_label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
        records_row.addWidget(records_label)
        
        self.records_spin = QSpinBox()
        self.records_spin.setRange(1, 10000)
        self.records_spin.setValue(1000)
        self.records_spin.setFixedHeight(35)
        self.records_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 5px 10px;
                color: black;
                font-size: 10px;
            }
            QSpinBox:hover {
                border: 1px solid #0078d4;
            }
        """)
        records_row.addWidget(self.records_spin)
        records_row.addStretch()
        options_layout.addLayout(records_row)
        
        layout.addWidget(options_container)
        
        self.preview_text = QTextEdit()
        self.preview_text.setFixedHeight(300)
        self.preview_text.setPlaceholderText("Data preview will appear here...")
        self.preview_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 10px;
                color: black;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.preview_text)
        
        button_row = QHBoxLayout()
        
        self.preview_button = QPushButton("Generate Preview")
        self.preview_button.setFixedHeight(40)
        self.preview_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.preview_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
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
        button_row.addWidget(self.preview_button)
        
        self.export_button = QPushButton("Export Data")
        self.export_button.setFixedHeight(40)
        self.export_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
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
        button_row.addWidget(self.export_button)
        
        button_row.addStretch()
        layout.addLayout(button_row)
        
        layout.addStretch()