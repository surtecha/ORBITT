from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotTile(QWidget):
    def __init__(self, title: str, x_data, y_data, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label)

        # Create matplotlib figure
        self.figure = Figure(figsize=(2, 2))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot(x_data, y_data)

    def plot(self, x, y):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, marker='o', linewidth=1)
        ax.set_xticks([])  # Hide ticks for preview
        ax.set_yticks([])
        ax.set_title("", pad=5)
        self.canvas.draw()
