from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QSpinBox
from PySide6.QtCore import Qt

class SliderInputField(QWidget):
    def __init__(self, label_text="", min_value=1, max_value=100, step=1, default=None, parent=None):
        super().__init__(parent)
        self.layout = None
        self.label = None
        self.slider = None
        self.spinbox = None
        self.setup_ui(label_text, min_value, max_value, step, default)

    def setup_ui(self, label_text, min_value, max_value, step, default):
        default_value = default if default is not None else (min_value + max_value) // 2

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if label_text:
            self.label = QLabel(label_text)
            self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(min_value, max_value)
        self.slider.setSingleStep(step)
        self.slider.setValue(default_value)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(min_value, max_value)
        self.spinbox.setSingleStep(step)
        self.spinbox.setValue(default_value)
        self.spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinbox.setMaximumWidth(self.spinbox.sizeHint().width())

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel(str(min_value)))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(QLabel(str(max_value)))
        slider_layout.addWidget(self.spinbox)

        self.layout.addLayout(slider_layout)

        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)

    def value(self):
        return self.slider.value()