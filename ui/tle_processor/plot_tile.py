from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor, QPainter, QPen
import random

class PlotTile(QWidget):
    tile_clicked = pyqtSignal(str)
    
    def __init__(self, plot_name):
        super().__init__()
        self.plot_name = plot_name
        self.is_hovered = False
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(280, 200)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.chart_area = QWidget()
        self.chart_area.setFixedHeight(150)
        self.chart_area.setStyleSheet("background-color: #f8f9fa; border: none;")
        layout.addWidget(self.chart_area)
        
        label_container = QWidget()
        label_container.setFixedHeight(50)
        label_container.setStyleSheet("background-color: white; border: none;")
        label_layout = QVBoxLayout(label_container)
        label_layout.setContentsMargins(15, 10, 15, 10)
        
        self.label = QLabel(self.plot_name)
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setWeight(QFont.Medium)
        self.label.setFont(label_font)
        self.label.setStyleSheet("color: black; background: transparent; border: none;")
        self.label.setAlignment(Qt.AlignCenter)
        label_layout.addWidget(self.label)
        
        layout.addWidget(label_container)
        
        self.update_style()
        
    def update_style(self):
        if self.is_hovered:
            self.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 2px solid #0078d4;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    border-radius: 8px;
                }
            """)
            
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self.chart_area)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.chart_area.rect()
        margin = 20
        chart_rect = rect.adjusted(margin, margin, -margin, -margin)
        
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.blue)
        painter.setPen(pen)
        
        points = []
        random.seed(hash(self.plot_name))
        
        for i in range(20):
            x = chart_rect.left() + (i * chart_rect.width() / 19)
            y = chart_rect.center().y() + random.randint(-40, 40)
            points.append((x, y))
            
        for i in range(len(points) - 1):
            painter.drawLine(int(points[i][0]), int(points[i][1]), 
                           int(points[i+1][0]), int(points[i+1][1]))
            
        pen.setWidth(4)
        painter.setPen(pen)
        for x, y in points:
            painter.drawPoint(int(x), int(y))
            
    def enterEvent(self, event):
        self.is_hovered = True
        self.update_style()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.is_hovered = False
        self.update_style()
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.tile_clicked.emit(self.plot_name)
        super().mousePressEvent(event)