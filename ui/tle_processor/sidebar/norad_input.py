from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator

class NoradInput(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        label = QLabel("NORAD ID")
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Medium)
        label.setFont(font)
        label.setStyleSheet("color: black; background: transparent; border: none;")
        layout.addWidget(label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter NORAD ID...")
        self.input_field.setFixedHeight(35)
        
        validator = QIntValidator(1, 99999999)
        self.input_field.setValidator(validator)
        
        input_font = QFont()
        input_font.setPointSize(10)
        self.input_field.setFont(input_font)
        
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px 12px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                outline: none;
            }
            QLineEdit:hover {
                border: 1px solid #808080;
            }
        """)
        
        layout.addWidget(self.input_field)
        
    def get_norad_id(self):
        text = self.input_field.text().strip()
        if text:
            try:
                return int(text)
            except ValueError:
                return None
        return None
        
    def set_norad_id(self, norad_id):
        if norad_id is not None:
            self.input_field.setText(str(norad_id))
        else:
            self.input_field.clear()
            
    def clear(self):
        self.input_field.clear()