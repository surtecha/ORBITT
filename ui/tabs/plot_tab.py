from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui.dialogs.plot_detail_window import PlotDetailWindow


def create_plot_widget(dataframe):
    column_headers = {
        'time': 'Epoch',
        'a': 'Semi Major Axis (km)',
        'apogee': 'Apogee (km)',
        'perigee': 'Perigee (km)',
        'e': 'Eccentricity',
        'i': 'Inclination (deg)',
        'raan': 'RAAN (deg)',
        'aop': 'Arg of Perigee (deg)',
        'ma': 'Mean Anomaly (deg)',
        'bstar': 'B-Star',
        'mean_motion': 'Mean Motion (rev/day)',
        'mean_motion_derivative': 'Mean Motion Deriv (rev/day²)',
        'revolution_number': 'Revolution Number'
    }
    
    widget = QWidget()
    layout = QGridLayout(widget)
    layout.setSpacing(10)
    layout.setContentsMargins(10, 10, 10, 10)
    
    time_data = dataframe['time']
    plot_params = [col for col in dataframe.columns if col != 'time']
    
    row, col = 0, 0
    for param in plot_params:
        param_label = column_headers.get(param, param)
        param_data = dataframe[param]
        
        preview_widget = _create_preview_plot(time_data, param_data, param, param_label)
        layout.addWidget(preview_widget, row, col)
        
        col += 1
        if col >= 3:
            col = 0
            row += 1
    
    return widget


def _create_preview_plot(time_data, param_data, param_name, param_label):
    container = QWidget()
    container.setMinimumSize(300, 200)
    container.setCursor(Qt.PointingHandCursor)
    
    container_layout = QGridLayout(container)
    container_layout.setContentsMargins(5, 5, 5, 5)
    
    figure = Figure(figsize=(3, 2))
    canvas = FigureCanvas(figure)
    canvas.setCursor(Qt.PointingHandCursor)
    
    ax = figure.add_subplot(111)
    ax.plot(time_data, param_data, linewidth=1, color='#2E86AB')
    ax.set_title(param_label, fontsize=9, fontweight='bold')
    
    ax.set_xticklabels([])
    ax.tick_params(axis='x', which='both', length=0)
    ax.tick_params(axis='y', labelsize=5)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    figure.tight_layout()
    canvas.draw()
    
    container_layout.addWidget(canvas, 0, 0)
    
    def on_click(event):
        _open_detail_window(time_data, param_data, param_name, param_label, container)
    
    canvas.mpl_connect('button_press_event', on_click)
    
    return container


def _open_detail_window(time_data, param_data, param_name, param_label, parent):
    detail_window = PlotDetailWindow(time_data, param_data, param_name, param_label, parent)
    detail_window.exec()

