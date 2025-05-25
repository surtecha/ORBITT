from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QGroupBox
from PyQt5.QtCore import Qt
from .norad_input import NoradInput
from .filter_widget import FilterWidget
from .slider_widget import SliderWidget
from .search_button import SearchButton
from styles.stylesheet import get_widget_style

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(280)
        self.setStyleSheet(get_widget_style('sidebar'))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignTop)

        title_label = QLabel("Filter Options")
        title_label.setObjectName("sidebarTitleLabel")
        layout.addWidget(title_label)

        norad_group = QGroupBox("NORAD ID")
        norad_layout = QVBoxLayout(norad_group)
        self.norad_input = NoradInput()
        norad_layout.addWidget(self.norad_input)
        layout.addWidget(norad_group)

        filter_group = QGroupBox("Time Window")
        filter_layout = QVBoxLayout(filter_group)
        self.filter_widget = FilterWidget()
        filter_layout.addWidget(self.filter_widget)
        layout.addWidget(filter_group)
        
        slider_group = QGroupBox("Time Range")
        slider_layout = QVBoxLayout(slider_group)
        self.slider_widget = SliderWidget()
        slider_layout.addWidget(self.slider_widget)
        layout.addWidget(slider_group)

        layout.addStretch(1)

        self.search_button = SearchButton()
        layout.addWidget(self.search_button)