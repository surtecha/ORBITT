from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

class SearchButton(QPushButton):
    search_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setText("Search TLEs")
        self.setFixedHeight(40)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Medium)
        self.setFont(font)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #c0c0c0;
                color: #808080;
            }
        """)
        
        self.clicked.connect(self.on_clicked)
        
    def on_clicked(self):
        self.search_clicked.emit()
        
    def set_loading(self, is_loading):
        if is_loading:
            self.setText("Searching...")
            self.setEnabled(False)
        else:
            self.setText("Search TLEs")
            self.setEnabled(True)