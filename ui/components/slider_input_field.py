from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QSpinBox
from PySide6.QtCore import Qt

class SliderInputField(QWidget):
    def __init__(self, min_value=1, max_value=100, step=1, default=None, parent=None):
        super().__init__(parent)

        # Set default value
        default_value = default if default is not None else (min_value + max_value) // 2

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(min_value, max_value)
        self.slider.setSingleStep(step)
        self.slider.setValue(default_value)

        # SpinBox
        self.spinbox = QSpinBox()
        self.spinbox.setRange(min_value, max_value)
        self.spinbox.setSingleStep(step)
        self.spinbox.setValue(default_value)
        self.spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout for slider with min/max labels
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel(str(min_value)))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(QLabel(str(max_value)))

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(slider_layout)
        self.layout.addWidget(self.spinbox)
        self.setLayout(self.layout)

        # Connect slider <-> spinbox
        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)

    def value(self):
        return self.slider.value()
