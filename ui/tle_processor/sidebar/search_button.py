from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from styles.stylesheet import get_button_style

class SearchButton(QPushButton):
    search_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setText("Search TLEs")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet(get_button_style('primary'))
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