from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


def create_propagation_widget(data):
    # Placeholder - to be implemented
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    label = QLabel("Propagation functionality coming soon...")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)
    
    return widget
