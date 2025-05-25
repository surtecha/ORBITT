from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from .category_widget import CategoryWidget

class PlotArea(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(30)
        content_layout.setAlignment(Qt.AlignTop)

        categories = [
            ("Altitude", ["Apogee", "Perigee"]),
            ("Angular Elements", ["Inclination", "RAAN", "Argument of Perigee", "Mean Anomaly"]),
            ("Shape and Size", ["Eccentricity", "Semi-major Axis"]),
            ("Drag", ["Drag Coefficient", "Ballistic Coefficient"]),
            ("Miscellaneous", ["Mean Motion", "Period", "Decay Rate"])
        ]

        for category_name, plot_names in categories:
            category_widget = CategoryWidget(category_name, plot_names)
            content_layout.addWidget(category_widget)

        content_layout.addStretch(1)
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)