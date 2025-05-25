from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from .plot_tile import PlotTile

class CategoryWidget(QWidget):
    def __init__(self, category_name, plot_names):
        super().__init__()
        self.category_name = category_name
        self.plot_names = plot_names
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.title_label = QLabel(self.category_name)
        self.title_label.setObjectName("categoryTitleLabel")
        layout.addWidget(self.title_label)

        tiles_container = QWidget()
        tiles_layout = QGridLayout(tiles_container)
        tiles_layout.setContentsMargins(0, 0, 0, 0)
        tiles_layout.setSpacing(15)

        columns = 3

        for i, plot_name in enumerate(self.plot_names):
            row = i // columns
            col = i % columns
            plot_tile = PlotTile(plot_name)
            tiles_layout.addWidget(plot_tile, row, col, Qt.AlignTop)

        num_items_last_row = len(self.plot_names) % columns
        if num_items_last_row != 0:
            for col_idx in range(num_items_last_row, columns):
                 tiles_layout.addItem(QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Preferred), len(self.plot_names) // columns, col_idx)

        for col in range(columns):
            tiles_layout.setColumnStretch(col, 1)

        layout.addWidget(tiles_container)
        layout.addStretch(1)