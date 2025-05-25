from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor, QPainter, QPen
import random

class FullscreenPlot(QDialog):
    def __init__(self, plot_name, parent=None):
        super().__init__(parent)
        self.plot_name = plot_name
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f"ORBITT - {self.plot_name}")
        self.setModal(True)
        self.showMaximized()
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #d0d0d0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        title_label = QLabel(self.plot_name)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: black; background: transparent; border: none;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(80, 35)
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        close_font = QFont()
        close_font.setPointSize(10)
        close_font.setWeight(QFont.Medium)
        self.close_button.setFont(close_font)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #808080;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        self.close_button.clicked.connect(self.close)
        header_layout.addWidget(self.close_button)
        
        layout.addWidget(header)
        
        self.plot_widget = FullscreenPlotWidget(self.plot_name)
        layout.addWidget(self.plot_widget, 1)
        
        controls_panel = QWidget()
        controls_panel.setFixedHeight(80)
        controls_panel.setStyleSheet("background-color: #f8f9fa; border-top: 1px solid #d0d0d0;")
        controls_layout = QHBoxLayout(controls_panel)
        controls_layout.setContentsMargins(20, 15, 20, 15)
        
        controls_label = QLabel("Interactive Controls:")
        controls_font = QFont()
        controls_font.setPointSize(11)
        controls_font.setWeight(QFont.Medium)
        controls_label.setFont(controls_font)
        controls_label.setStyleSheet("color: black; background: transparent; border: none;")
        controls_layout.addWidget(controls_label)
        
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.setFixedSize(80, 30)
        self.zoom_in_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.zoom_in_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        controls_layout.addWidget(self.zoom_in_button)
        
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.setFixedSize(80, 30)
        self.zoom_out_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.zoom_out_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        controls_layout.addWidget(self.zoom_out_button)
        
        self.reset_button = QPushButton("Reset View")
        self.reset_button.setFixedSize(80, 30)
        self.reset_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        controls_layout.addWidget(self.reset_button)
        
        controls_layout.addStretch()
        
        info_label = QLabel("Left click and drag to pan • Mouse wheel to zoom • Right click for options")
        info_font = QFont()
        info_font.setPointSize(9)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: #666666; background: transparent; border: none;")
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
        
        self.setStyleSheet("background-color: white; border: none;")
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        margin = int(60 * self.zoom_factor)
        chart_rect = rect.adjusted(margin + self.pan_x, margin + self.pan_y, 
                                 -margin + self.pan_x, -margin + self.pan_y)
        
        painter.fillRect(rect, Qt.white)
        
        grid_pen = QPen()
        grid_pen.setWidth(1)
        grid_pen.setColor(Qt.lightGray)
        grid_pen.setStyle(Qt.DashLine)
        painter.setPen(grid_pen)
        
        grid_spacing = int(50 * self.zoom_factor)
        for x in range(chart_rect.left(), chart_rect.right(), grid_spacing):
            painter.drawLine(x, chart_rect.top(), x, chart_rect.bottom())
        for y in range(chart_rect.top(), chart_rect.bottom(), grid_spacing):
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)
        
        axis_pen = QPen()
        axis_pen.setWidth(2)
        axis_pen.setColor(Qt.black)
        painter.setPen(axis_pen)
        
        painter.drawLine(chart_rect.left(), chart_rect.bottom(), chart_rect.right(), chart_rect.bottom())
        painter.drawLine(chart_rect.left(), chart_rect.top(), chart_rect.left(), chart_rect.bottom())
        
        data_pen = QPen()
        data_pen.setWidth(int(3 * self.zoom_factor))
        data_pen.setColor(Qt.blue)
        painter.setPen(data_pen)
        
        points = []
        random.seed(hash(self.plot_name))
        
        num_points = 50
        for i in range(num_points):
            x = chart_rect.left() + (i * chart_rect.width() / (num_points - 1))
            base_y = chart_rect.center().y()
            variation = random.randint(-int(chart_rect.height() * 0.3), int(chart_rect.height() * 0.3))
            y = base_y + variation
            points.append((x, y))
            
        for i in range(len(points) - 1):
            painter.drawLine(int(points[i][0]), int(points[i][1]), 
                           int(points[i+1][0]), int(points[i+1][1]))
            
        point_pen = QPen()
        point_pen.setWidth(int(6 * self.zoom_factor))
        point_pen.setColor(Qt.darkBlue)
        painter.setPen(point_pen)
        
        for x, y in points[::3]:
            painter.drawPoint(int(x), int(y))
        
    def wheelEvent(self, event):
        zoom_in = event.angleDelta().y() > 0
        zoom_step = 0.1
        
        if zoom_in:
            self.zoom_factor = min(3.0, self.zoom_factor + zoom_step)
        else:
            self.zoom_factor = max(0.3, self.zoom_factor - zoom_step)
            
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_pan_point = event.pos()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            
    def mouseMoveEvent(self, event):
        if self.dragging and self.last_pan_point:
            delta = event.pos() - self.last_pan_point
            self.pan_x += delta.x()
            self.pan_y += delta.y()
            self.last_pan_point = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            
    def zoom_in(self):
        self.zoom_factor = min(3.0, self.zoom_factor + 0.2)
        self.update()
        
    def zoom_out(self):
        self.zoom_factor = max(0.3, self.zoom_factor - 0.2)
        self.update()
        
    def reset_view(self):
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.update()