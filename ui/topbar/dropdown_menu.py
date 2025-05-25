from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class DropdownMenu(QComboBox):
    selection_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(150, 30)
        
        font = QFont()
        font.setPointSize(10)
        font.setWeight(QFont.Medium)
        self.setFont(font)
        
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 5px 10px;
                color: black;
            }
            QComboBox:hover {
                border: 1px solid #0078d4;
            }
            QComboBox:focus {
                border: 2px solid #0078d4;
                outline: none;
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
                selection-color: black;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 10px;
                border: none;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f0f0f0;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)
        
        self.addItems(["Visualize", "Neural Network"])
        self.setCurrentText("Visualize")
        
        self.currentTextChanged.connect(self.on_selection_changed)
        
    def on_selection_changed(self, text):
        self.selection_changed.emit(text)
        
    def set_selection(self, text):
        index = self.findText(text)
        if index >= 0:
            self.setCurrentIndex(index)