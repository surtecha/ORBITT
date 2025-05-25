from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

class NoradInput(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter NORAD ID...")

        validator = QIntValidator(1, 99999999)
        self.input_field.setValidator(validator)

        layout.addWidget(self.input_field)

    def get_norad_id(self):
        text = self.input_field.text().strip()
        if text:
            try:
                return int(text)
            except ValueError:
                return None
        return None

    def set_norad_id(self, norad_id):
        if norad_id is not None:
            self.input_field.setText(str(norad_id))
        else:
            self.input_field.clear()

    def clear(self):
        self.input_field.clear()