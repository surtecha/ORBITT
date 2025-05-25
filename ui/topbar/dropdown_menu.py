from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal

class DropdownMenu(QComboBox):
    selection_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(180)
        
        self.addItems(["Visualize", "Neural Network"])
        self.setCurrentText("Visualize")

        self.currentTextChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, text):
        self.selection_changed.emit(text)

    def set_selection(self, text):
        index = self.findText(text)
        if index >= 0:
            if self.currentIndex() != index:
                self.setCurrentIndex(index)