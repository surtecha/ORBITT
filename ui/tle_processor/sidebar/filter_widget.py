from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

class FilterWidget(QWidget):
    filter_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        options = [
            ("Days", "days"),
            ("Weeks", "weeks"),
            ("Months", "months")
        ]

        radio_button_layout = QVBoxLayout()
        radio_button_layout.setSpacing(5)

        for i, (display_text, value) in enumerate(options):
            radio_button = QRadioButton(display_text)
            radio_button.setProperty("value", value)

            self.button_group.addButton(radio_button, i)
            radio_button_layout.addWidget(radio_button)

            if i == 0:
                radio_button.setChecked(True)

        layout.addLayout(radio_button_layout)

        self.button_group.buttonClicked.connect(self.on_button_clicked)

    def on_button_clicked(self, button):
        value = button.property("value")
        self.filter_changed.emit(value)

    def get_selected_filter(self):
        checked_button = self.button_group.checkedButton()
        if checked_button:
            return checked_button.property("value")
        return "days"

    def set_filter(self, filter_value):
        for button in self.button_group.buttons():
            if button.property("value") == filter_value:
                button.setChecked(True)
                break