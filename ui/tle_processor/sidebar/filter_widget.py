from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class FilterWidget(QWidget):
    filter_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        label = QLabel("Time Window")
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Medium)
        label.setFont(font)
        label.setStyleSheet("color: black; background: transparent; border: none;")
        layout.addWidget(label)
        
        self.button_group = QButtonGroup(self)
        
        options = [
            ("Days", "days"),
            ("Weeks", "weeks"),
            ("Months", "months")
        ]
        
        for i, (display_text, value) in enumerate(options):
            radio_button = QRadioButton(display_text)
            radio_button.setProperty("value", value)
            
            button_font = QFont()
            button_font.setPointSize(10)
            radio_button.setFont(button_font)
            
            radio_button.setStyleSheet("""
                QRadioButton {
                    color: black;
                    background: transparent;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #c0c0c0;
                    border-radius: 8px;
                    background-color: white;
                }
                QRadioButton::indicator:unchecked:hover {
                    border: 2px solid #808080;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #0078d4;
                    border-radius: 8px;
                    background-color: white;
                }
                QRadioButton::indicator:checked:after {
                    width: 8px;
                    height: 8px;
                    border-radius: 4px;
                    background-color: #0078d4;
                    margin: 2px;
                }
            """)
            
            self.button_group.addButton(radio_button, i)
            layout.addWidget(radio_button)
            
            if i == 0:
                radio_button.setChecked(True)
                
        self.button_group.buttonClicked.connect(self.on_button_clicked)
        
    def on_button_clicked(self, button):
        value = button.property("value")
        self.filter_changed.emit(value)
        
    def get_selected_filter(self):
        checked_button = self.button_group.checkedButton()
        if checked_button:
            return checked_button.property("value")
        return "days"
        
    def set_filter(self, filter_value):
        for button in self.button_group.buttons():
            if button.property("value") == filter_value:
                button.setChecked(True)
                break