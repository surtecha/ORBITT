from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import matplotlib.pyplot as plt
import io


class Tile(QFrame):
    clicked = Signal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedSize(320, 280)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                background-color: #ffffff;
            }
            QFrame:hover {
                border-color: #3b82f6;
                background-color: #f8fafc;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        self.plot_label = QLabel()
        self.plot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plot_label.setFixedSize(304, 230)
        self.plot_label.setStyleSheet("""
            QLabel {
                border: none;
                border-radius: 8px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.plot_label)

        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet("""
            QLabel {
                border: none;
                font-weight: 600;
                font-size: 12px;
                color: #374151;
                background-color: transparent;
            }
        """)
        layout.addWidget(self.title_label)

    def set_matplotlib_figure(self, figure):
        buf = io.BytesIO()
        figure.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                      facecolor='white', edgecolor='none', pad_inches=0.05)
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        scaled_pixmap = pixmap.scaled(
            304, 230,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.plot_label.setPixmap(scaled_pixmap)
        plt.close(figure)
        buf.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)