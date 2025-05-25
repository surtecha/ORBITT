from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal

class SliderWidget(QWidget):
    value_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        self.value_label = QLabel("7")
        self.value_label.setObjectName("valueLabel")
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        slider_control_layout = QHBoxLayout()
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setValue(7)
        slider_control_layout.addWidget(self.slider, 1)
        
        slider_control_layout.addSpacing(10)
        slider_control_layout.addWidget(self.value_label)
        
        layout.addLayout(slider_control_layout)

        range_layout = QHBoxLayout()
        min_label = QLabel("1")
        min_label.setObjectName("minLabel")
        range_layout.addWidget(min_label, 0, Qt.AlignLeft)

        range_layout.addStretch(1)

        max_label = QLabel("30")
        max_label.setObjectName("maxLabel")
        range_layout.addWidget(max_label, 0, Qt.AlignRight)

        layout.addLayout(range_layout)

        self.slider.valueChanged.connect(self.on_value_changed)
        self.on_value_changed(self.slider.value())

    def on_value_changed(self, value):
        self.value_label.setText(str(value))
        self.value_changed.emit(value)

    def get_value(self):
        return self.slider.value()

    def set_value(self, value):
        clamped_value = max(self.slider.minimum(), min(value, self.slider.maximum()))
        self.slider.setValue(clamped_value)