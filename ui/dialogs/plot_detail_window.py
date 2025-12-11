from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QColorDialog, QLineEdit, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlotDetailWindow(QDialog):
    def __init__(self, time_data, param_data, param_name, param_label, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"{param_label} vs Time")
        self.resize(900, 600)
        
        self.time_data = time_data
        self.param_data = param_data
        self.param_name = param_name
        self.param_label = param_label
        
        self.show_markers = False
        self.plot_color = '#2E86AB'
        self.custom_title = f'{param_label} vs Time'
        self.show_title = True
        self.initial_render = True
        
        layout = QVBoxLayout(self)
        
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        controls_layout = QHBoxLayout()
        
        self.marker_checkbox = QCheckBox("Show Markers")
        self.marker_checkbox.setChecked(False)
        self.marker_checkbox.stateChanged.connect(self._toggle_markers)
        controls_layout.addWidget(self.marker_checkbox)
        
        self.color_button = QPushButton("Select Color")
        self.color_button.clicked.connect(self._select_color)
        controls_layout.addWidget(self.color_button)
        
        controls_layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setText(self.custom_title)
        self.title_input.setMaximumWidth(250)
        self.title_input.textChanged.connect(self._update_title)
        controls_layout.addWidget(self.title_input)
        
        self.title_checkbox = QCheckBox("Show Title")
        self.title_checkbox.setChecked(True)
        self.title_checkbox.stateChanged.connect(self._toggle_title)
        controls_layout.addWidget(self.title_checkbox)
        
        controls_layout.addStretch()
        
        layout.addWidget(self.toolbar)
        layout.addLayout(controls_layout)
        layout.addWidget(self.canvas)
        
        self._plot_data()
    
    def showEvent(self, event):
        super().showEvent(event)
        if self.initial_render:
            self.initial_render = False
            QTimer.singleShot(10, self._refresh_plot)
    
    def _refresh_plot(self):
        self.figure.tight_layout()
        self.canvas.draw()
    
    def _toggle_markers(self, state):
        self.show_markers = state == 2
        self._plot_data()
    
    def _select_color(self):
        color = QColorDialog.getColor(QColor(self.plot_color), self, "Select Plot Color")
        if color.isValid():
            self.plot_color = color.name()
            self._plot_data()
    
    def _update_title(self, text):
        self.custom_title = text
        if self.show_title:
            self._plot_data()
    
    def _toggle_title(self, state):
        self.show_title = state == 2
        self._plot_data()
    
    def _plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if self.show_markers:
            ax.plot(self.time_data, self.param_data, linewidth=1.5, color=self.plot_color, 
                   marker='o', markersize=4, markerfacecolor=self.plot_color, markeredgecolor='white', markeredgewidth=0.5)
        else:
            ax.plot(self.time_data, self.param_data, linewidth=1.5, color=self.plot_color)
        
        ax.set_xlabel('Time', fontsize=11)
        ax.set_ylabel(self.param_label, fontsize=11)
        
        if self.show_title and self.custom_title:
            ax.set_title(self.custom_title, fontsize=13, fontweight='bold')
        
        ax.tick_params(axis='x', labelsize=8, rotation=45)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(10))
        
        self.figure.tight_layout()
        self.canvas.draw()
