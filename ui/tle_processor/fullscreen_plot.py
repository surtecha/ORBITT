from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QCursor, QPainter, QPen, QPainterPath, QColor
import random
from styles.stylesheet import get_widget_style, get_button_style

class FullscreenPlot(QDialog):
    def __init__(self, plot_name, parent=None):
        super().__init__(parent)
        self.plot_name = plot_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"ORBITT - {self.plot_name}")
        self.setModal(True)
        self.resize(1200, 800)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet(get_widget_style('fullscreen_header'))
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)

        title_label = QLabel(self.plot_name)
        title_label.setObjectName("fullscreenPlotTitleLabel")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        self.close_button = QPushButton("Close")
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_button.setStyleSheet(get_button_style('secondary'))
        self.close_button.clicked.connect(self.close)
        header_layout.addWidget(self.close_button)

        layout.addWidget(header)

        self.plot_widget = FullscreenPlotWidget(self.plot_name)
        layout.addWidget(self.plot_widget, 1)

        controls_panel = QWidget()
        controls_panel.setStyleSheet(get_widget_style('fullscreen_controls'))
        controls_layout = QHBoxLayout(controls_panel)
        controls_layout.setContentsMargins(20, 15, 20, 15)
        controls_layout.setSpacing(10)

        controls_label = QLabel("Interactive Controls:")
        controls_label.setObjectName("fullscreenControlsLabel")
        controls_layout.addWidget(controls_label)

        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.zoom_in_button.setStyleSheet(get_button_style('button_small_secondary'))
        controls_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.zoom_out_button.setStyleSheet(get_button_style('button_small_secondary'))
        controls_layout.addWidget(self.zoom_out_button)

        self.reset_button = QPushButton("Reset View")
        self.reset_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.reset_button.setStyleSheet(get_button_style('button_small_primary'))
        controls_layout.addWidget(self.reset_button)

        controls_layout.addStretch()

        info_label = QLabel("Left click & drag: Pan • Mouse wheel: Zoom • Right click: Options")
        info_label.setObjectName("fullscreenInfoLabel")
        controls_layout.addWidget(info_label)

        layout.addWidget(controls_panel)

        self.zoom_in_button.clicked.connect(self.plot_widget.zoom_in)
        self.zoom_out_button.clicked.connect(self.plot_widget.zoom_out)
        self.reset_button.clicked.connect(self.plot_widget.reset_view)

class FullscreenPlotWidget(QWidget):
    def __init__(self, plot_name):
        super().__init__()
        self.plot_name = plot_name
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.last_pan_point = None
        self.dragging = False
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: white;")


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, Qt.white)

        margin = int(max(20, 50 * self.zoom_factor))
        chart_rect = rect.adjusted(
            margin + self.pan_x, margin + self.pan_y,
            -margin + self.pan_x, -margin + self.pan_y
        )

        if not chart_rect.isValid() or chart_rect.width() < 10 or chart_rect.height() < 10:
            painter.drawText(rect, Qt.AlignCenter, "Zoom or pan to view chart.")
            return

        grid_pen = QPen(Qt.lightGray, 1, Qt.DotLine)
        painter.setPen(grid_pen)
        grid_spacing = max(20, int(50 * self.zoom_factor))
        if grid_spacing > 5:
            x_start = chart_rect.left() - (chart_rect.left() % grid_spacing)
            for x in range(int(x_start), chart_rect.right(), grid_spacing):
                if x >= chart_rect.left(): painter.drawLine(x, chart_rect.top(), x, chart_rect.bottom())
            y_start = chart_rect.top() - (chart_rect.top() % grid_spacing)
            for y in range(int(y_start), chart_rect.bottom(), grid_spacing):
                if y >= chart_rect.top(): painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)

        axis_pen = QPen(Qt.black, 1.5)
        painter.setPen(axis_pen)
        painter.drawLine(chart_rect.left(), chart_rect.bottom(), chart_rect.right(), chart_rect.bottom())
        painter.drawLine(chart_rect.left(), chart_rect.top(), chart_rect.left(), chart_rect.bottom())

        data_pen = QPen(QColor("#007aff"), max(1, int(2 * self.zoom_factor)))
        painter.setPen(data_pen)
        points = []
        random.seed(hash(self.plot_name))
        num_points = 50
        if num_points > 1:
            for i in range(num_points):
                x_pos = chart_rect.left() + (i * chart_rect.width() / (num_points - 1))
                y_offset = random.randint(-int(chart_rect.height() * 0.35), int(chart_rect.height() * 0.35))
                y_pos = chart_rect.center().y() + y_offset
                points.append(QPointF(x_pos, y_pos))

            if points:
                path = QPainterPath()
                path.moveTo(points[0])
                for i in range(1, len(points)):
                    path.lineTo(points[i])
                painter.drawPath(path)


    def wheelEvent(self, event):
        zoom_step = 0.15
        old_zoom = self.zoom_factor
        mouse_point = event.pos()

        if event.angleDelta().y() > 0:
            self.zoom_factor = min(10.0, self.zoom_factor * (1 + zoom_step))
        else:
            self.zoom_factor = max(0.1, self.zoom_factor / (1 + zoom_step))

        dx_scene_before = (mouse_point.x() - self.pan_x) / old_zoom
        dy_scene_before = (mouse_point.y() - self.pan_y) / old_zoom

        self.pan_x = mouse_point.x() - dx_scene_before * self.zoom_factor
        self.pan_y = mouse_point.y() - dy_scene_before * self.zoom_factor

        self.update()
        super().wheelEvent(event)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_pan_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging and self.last_pan_point is not None:
            delta = event.pos() - self.last_pan_point
            self.pan_x += delta.x()
            self.pan_y += delta.y()
            self.last_pan_point = event.pos()
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.last_pan_point = None
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def zoom_in(self):
        self.zoom_factor = min(10.0, self.zoom_factor * 1.2)
        self.update()

    def zoom_out(self):
        self.zoom_factor = max(0.1, self.zoom_factor / 1.2)
        self.update()

    def reset_view(self):
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.update()