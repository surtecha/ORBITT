from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .plot_tile import PlotTile

class CategoryWidget(QWidget):
    def __init__(self, category_name, plot_names):
        super().__init__()
        self.category_name = category_name
        self.plot_names = plot_names
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        title_label = QLabel(self.category_name)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: black; background: transparent; border: none; margin-bottom: 5px;")
        layout.addWidget(title_label)
        
        tiles_container = QWidget()
        tiles_container.setStyleSheet("background-color: transparent; border: none;")
        tiles_layout = QGridLayout(tiles_container)
        tiles_layout.setContentsMargins(0, 0, 0, 0)
        tiles_layout.setSpacing(15)
        
        columns = min(3, len(self.plot_names))
        
        for i, plot_name in enumerate(self.plot_names):
            row = i // columns
            col = i % columns
            
            plot_tile = PlotTile(plot_name)
            tiles_layout.addWidget(plot_tile, row, col)
            
        for col in range(columns):
            tiles_layout.setColumnStretch(col, 1)
            
        layout.addWidget(tiles_container)