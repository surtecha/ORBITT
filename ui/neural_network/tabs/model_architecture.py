from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ModelArchitecture(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel("Neural Network - Model Architecture Tab (Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)