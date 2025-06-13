from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator

class InputField(QWidget):
    def __init__(self, label_text="", placeholder="", parent=None):
        super().__init__(parent)
        self.layout = None
        self.label = None
        self.line_edit = None
        self.setup_ui(label_text, placeholder)

    def setup_ui(self, label_text, placeholder):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if label_text:
            self.label = QLabel(label_text)
            self.layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.layout.addWidget(self.line_edit)

        validator = QIntValidator()
        self.line_edit.setValidator(validator)

    def text(self):
        return self.line_edit.text()

    def set_text(self, text):
        self.line_edit.setText(text)