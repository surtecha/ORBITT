from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from PyQt5.QtGui import QCursor, QPainter, QPen, QPainterPath, QColor
import random
from styles.stylesheet import get_widget_style

class PlotTile(QWidget):
    tile_clicked = pyqtSignal(str)

    def __init__(self, plot_name):
        super().__init__()
        self.plot_name = plot_name
        self.is_hovered = False
        self.init_ui()
        self.setMouseTracking(True)

    def init_ui(self):
        self.setFixedSize(280, 200)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.chart_area = QWidget()
        self.chart_area.setFixedHeight(150)
        self.chart_area.setObjectName("plotTileChartArea")
        self.chart_area.setStyleSheet(get_widget_style('chart_placeholder'))
        layout.addWidget(self.chart_area)

        label_container = QWidget()
        label_layout = QVBoxLayout(label_container)
        label_layout.setContentsMargins(15, 10, 15, 10)
        label_layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self.plot_name)
        self.label.setAlignment(Qt.AlignCenter)
        label_layout.addWidget(self.label)

        layout.addWidget(label_container)
        self.update_style()


    def update_style(self):
        if self.is_hovered:
            self.setStyleSheet(get_widget_style('card_hover'))
        else:
            self.setStyleSheet(get_widget_style('card'))
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.label.update()


    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self.chart_area)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.chart_area.rect()

        margin = 15
        chart_rect = rect.adjusted(margin, margin, -margin, -margin)

        if not chart_rect.isValid() or chart_rect.width() < 5 or chart_rect.height() < 5:
            return

        pen_color = QColor("#007aff") if self.is_hovered else QColor("#a0a0a5")
        data_pen = QPen(pen_color, 1.5)
        painter.setPen(data_pen)

        points = []
        random.seed(hash(self.plot_name + "_tile"))

        num_points = 20
        if num_points > 1:
            for i in range(num_points):
                x = chart_rect.left() + (i * chart_rect.width() / (num_points - 1))
                y = chart_rect.center().y() + random.randint(-int(chart_rect.height()*0.3), int(chart_rect.height()*0.3))
                points.append(QPointF(x, y))

        if points:
            path = QPainterPath()
            path.moveTo(points[0])
            for i in range(1, len(points)):
                path.lineTo(points[i])
            painter.drawPath(path)


    def enterEvent(self, event):
        self.is_hovered = True
        self.update_style()
        self.chart_area.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update_style()
        self.chart_area.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.tile_clicked.emit(self.plot_name)
        super().mousePressEvent(event)