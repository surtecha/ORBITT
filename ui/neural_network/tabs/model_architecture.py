from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QTextEdit, QGroupBox, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

class ModelArchitecture(QWidget):
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
        
        title_label = QLabel("Neural Network Model Designer")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: black; background: transparent; border: none; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Design and configure neural network models for TLE prediction")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #666666; background: transparent; border: none; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
        main_container = QHBoxLayout()
        main_container.setSpacing(20)
        
        config_group = QGroupBox("Model Configuration")
        config_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: black;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
            }
        """)
        config_group.setFixedWidth(350)
        config_layout = QGridLayout(config_group)
        config_layout.setSpacing(15)
        
        model_type_label = QLabel("Model Type:")
        model_type_label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
        config_layout.addWidget(model_type_label, 0, 0)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["LSTM", "GRU", "Transformer", "CNN-LSTM"])
        self.model_combo.setFixedHeight(35)
        self.model_combo.setStyleSheet("""
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
        config_layout.addWidget(self.model_combo, 0, 1)
        
        layers_label = QLabel("Hidden Layers:")
        layers_label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
        config_layout.addWidget(layers_label, 1, 0)
        
        self.layers_spin = QSpinBox()
        self.layers_spin.setRange(1, 10)
        self.layers_spin.setValue(3)
        self.layers_spin.setFixedHeight(35)
        self.layers_spin.setStyleSheet("""
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
        config_layout.addWidget(self.layers_spin, 1, 1)
        
        neurons_label = QLabel("Neurons per Layer:")
        neurons_label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
        config_layout.addWidget(neurons_label, 2, 0)
        
        self.neurons_spin = QSpinBox()
        self.neurons_spin.setRange(10, 512)
        self.neurons_spin.setValue(64)
        self.neurons_spin.setSingleStep(16)
        self.neurons_spin.setFixedHeight(35)
        self.neurons_spin.setStyleSheet("""
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
        config_layout.addWidget(self.neurons_spin, 2, 1)
        
        epochs_label = QLabel("Training Epochs:")
        epochs_label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
        config_layout.addWidget(epochs_label, 3, 0)
        
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(10, 1000)
        self.epochs_spin.setValue(100)
        self.epochs_spin.setSingleStep(10)
        self.epochs_spin.setFixedHeight(35)
        self.epochs_spin.setStyleSheet("""
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
        config_layout.addWidget(self.epochs_spin, 3, 1)
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.build_button = QPushButton("Build Model")
        self.build_button.setFixedHeight(40)
        self.build_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.build_button.setStyleSheet("""
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
        button_layout.addWidget(self.build_button)
        
        self.train_button = QPushButton("Train Model")
        self.train_button.setFixedHeight(40)
        self.train_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.train_button.setStyleSheet("""
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
        button_layout.addWidget(self.train_button)
        
        config_layout.addLayout(button_layout, 4, 0, 1, 2)
        
        main_container.addWidget(config_group)
        
        architecture_group = QGroupBox("Model Architecture")
        architecture_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: black;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
            }
        """)
        architecture_layout = QVBoxLayout(architecture_group)
        
        self.architecture_text = QTextEdit()
        self.architecture_text.setFixedHeight(400)
        self.architecture_text.setPlaceholderText("Model architecture will be displayed here...")
        self.architecture_text.setReadOnly(True)
        self.architecture_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 10px;
                color: black;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        architecture_layout.addWidget(self.architecture_text)
        
        main_container.addWidget(architecture_group)
        
        layout.addLayout(main_container)
        layout.addStretch()