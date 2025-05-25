from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor

class Tab(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.is_active = False
        self.init_ui()
        
    def init_ui(self):
        self.setFixedHeight(35)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        
        self.label = QLabel(self.text)
        font = QFont()
        font.setPointSize(10)
        font.setWeight(QFont.Medium)
        self.label.setFont(font)
        
        layout.addWidget(self.label)
        
        self.update_style()
        
    def update_style(self):
        if self.is_active:
            self.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #c0c0c0;
                    border-bottom: 2px solid #0078d4;
                    border-radius: 6px 6px 0px 0px;
                }
                QLabel {
                    color: #0078d4;
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px 6px 0px 0px;
                }
                QWidget:hover {
                    background-color: #f0f0f0;
                    border: 1px solid #c0c0c0;
                }
                QLabel {
                    color: black;
                    border: none;
                    background: transparent;
                }
            """)
            
    def set_active(self, active):
        self.is_active = active
        self.update_style()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)