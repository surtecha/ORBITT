from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel

def get_sidebar_widgets():
    # Primary section: inputs and controls
    primary = [
        QLabel("Predictor"),
        QLineEdit("X-Axis"),
        QLineEdit("Y-Axis"),
        QPushButton("Plot")
    ]

    # Secondary section: output/info
    secondary = [
        QLabel("Status: Ready"),
        QLabel("Data Points: 0")
    ]

    return primary, secondary
