from PySide6.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QButtonGroup

class RadioButtonGroup(QWidget):
    def __init__(self, options=None, default_option=None, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.button_group = QButtonGroup(self)

        if options is None:
            options = ['D', 'W', 'M']
        default = default_option

        for option in options:
            btn = QRadioButton(option)
            self.layout.addWidget(btn)
            self.button_group.addButton(btn)

            if option == default:
                btn.setChecked(True)

    def selected(self):
        btn = self.button_group.checkedButton()
        return btn.text() if btn else None
