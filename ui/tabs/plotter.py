from ui.components.input_field import InputField
from ui.components.radio_button_group import RadioButtonGroup
from ui.components.slider_input_field import SliderInputField
from PySide6.QtWidgets import QLabel, QPushButton

def get_sidebar_widgets():
    primary = [
        InputField("NORAD ID", ""),
        RadioButtonGroup("Time Filter", options=["D", "W", "M"], default_option="D"),
        SliderInputField("", min_value=1, max_value=100, step=1, default=60),
        QPushButton("Plot")
    ]

    secondary = [
        QLabel("Last Epoch: "),
        QLabel("TLEs Obtained: ")
    ]

    return primary, secondary