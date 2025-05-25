from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .norad_input import NoradInput
from .filter_widget import FilterWidget
from .slider_widget import SliderWidget
from .search_button import SearchButton

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-right: 1px solid #d0d0d0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Filter Options")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: black; background: transparent; border: none;")
        layout.addWidget(title_label)
        
        self.norad_input = NoradInput()
        layout.addWidget(self.norad_input)
        
        self.filter_widget = FilterWidget()
        layout.addWidget(self.filter_widget)
        
        self.slider_widget = SliderWidget()
        layout.addWidget(self.slider_widget)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        self.search_button = SearchButton()
        layout.addWidget(self.search_button)
        
        bottom_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(bottom_spacer)