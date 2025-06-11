from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator

class InputField(QWidget):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)

        self.layout.addWidget(self.line_edit)
        self.setLayout(self.layout)

        validator = QIntValidator()
        self.line_edit.setValidator(validator)

    def text(self):
        return self.line_edit.text()

    def set_text(self, text):
        self.line_edit.setText(text)