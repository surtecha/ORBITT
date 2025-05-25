from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SliderWidget(QWidget):
    value_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Time Range")
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Medium)
        label.setFont(font)
        label.setStyleSheet("color: black; background: transparent; border: none;")
        header_layout.addWidget(label)
        
        header_layout.addStretch()
        
        self.value_label = QLabel("7")
        value_font = QFont()
        value_font.setPointSize(10)
        value_font.setWeight(QFont.Medium)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("color: #0078d4; background: transparent; border: none;")
        header_layout.addWidget(self.value_label)
        
        layout.addLayout(header_layout)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setValue(7)
        self.slider.setFixedHeight(25)
        
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #0078d4;
                border: 2px solid white;
                width: 20px;
                height: 20px;
                margin: -10px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: #106ebe;
                border: 2px solid white;
            }
            QSlider::handle:horizontal:pressed {
                background: #005a9e;
                border: 2px solid white;
            }
            QSlider::sub-page:horizontal {
                background: #0078d4;
                border-radius: 2px;
            }
        """)
        
        layout.addWidget(self.slider)
        
        range_layout = QHBoxLayout()
        range_layout.setContentsMargins(0, 0, 0, 0)
        
        min_label = QLabel("1")
        min_label.setStyleSheet("color: #808080; background: transparent; border: none; font-size: 9px;")
        range_layout.addWidget(min_label)
        
        range_layout.addStretch()
        
        max_label = QLabel("30")
        max_label.setStyleSheet("color: #808080; background: transparent; border: none; font-size: 9px;")
        range_layout.addWidget(max_label)
        
        layout.addLayout(range_layout)
        
        self.slider.valueChanged.connect(self.on_value_changed)
        
    def on_value_changed(self, value):
        self.value_label.setText(str(value))
        self.value_changed.emit(value)
        
    def get_value(self):
        return self.slider.value()
        
    def set_value(self, value):
        if 1 <= value <= 30:
            self.slider.setValue(value)