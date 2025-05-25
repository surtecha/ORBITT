from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from styles.stylesheet import get_tab_style

class Tab(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.is_active = False
        self.init_ui()
        self.setMouseTracking(True)

    def init_ui(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self.text)
        
        layout.addWidget(self.label)
        self.update_style()

    def update_style(self):
        self.setStyleSheet(get_tab_style(self.is_active))
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.label.update()


    def set_active(self, active):
        if self.is_active != active:
            self.is_active = active
            self.update_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.text)
        super().mousePressEvent(event)