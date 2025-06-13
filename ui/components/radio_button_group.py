from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QLabel

class RadioButtonGroup(QWidget):
    def __init__(self, label_text="", options=None, default_option=None, parent=None):
        super().__init__(parent)
        self.layout = None
        self.label = None
        self.buttons_layout = None
        self.button_group = None
        self.setup_ui(label_text, options, default_option)

    def setup_ui(self, label_text, options, default_option):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if label_text:
            self.label = QLabel(label_text)
            self.layout.addWidget(self.label)

        self.buttons_layout = QHBoxLayout()
        self.button_group = QButtonGroup(self)

        if options is None:
            options = ['D', 'W', 'M']

        for option in options:
            btn = QRadioButton(option)
            self.buttons_layout.addWidget(btn)
            self.button_group.addButton(btn)

            if option == default_option:
                btn.setChecked(True)

        self.layout.addLayout(self.buttons_layout)

    def selected(self):
        btn = self.button_group.checkedButton()
        return btn.text() if btn else None