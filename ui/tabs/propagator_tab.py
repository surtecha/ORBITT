from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider
from PySide6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from backend.utils.map_loader import MapLoader
import numpy as np


def create_propagator_widget(propagation_data, propagator_controller):
    widget = PropagatorWidget(propagation_data, propagator_controller)
    return widget


class PropagatorWidget(QWidget):
    def __init__(self, propagation_data, propagator_controller):
        super().__init__()

        self.propagation_data = propagation_data
        self.propagator_controller = propagator_controller
        self.trajectory = None
        self.current_index = 0
        self.is_playing = False

        map_loader = MapLoader()
        self.world = map_loader.get_world_map()

        self._setup_ui()
        self._setup_timer()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        controls_layout = self._create_controls()
        layout.addLayout(controls_layout)

        self.figure = Figure(figsize=(14, 10), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.figure.set_dpi(100)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout(pad=1.0)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.canvas.figure.savefig = self._custom_savefig
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self._draw_world_map()

    def _custom_savefig(self, *args, **kwargs):
        kwargs['dpi'] = 300
        return Figure.savefig(self.figure, *args, **kwargs)

    def _create_controls(self):
        main_controls = QVBoxLayout()
        main_controls.setSpacing(3)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        top_row.addWidget(QLabel("Start:"))
        self.start_time_input = QLineEdit()
        epoch = self.propagation_data['epoch']
        self.start_time_input.setText(epoch.strftime('%Y-%m-%d %H:%M:%S'))
        self.start_time_input.setReadOnly(True)
        self.start_time_input.setMaximumWidth(150)
        top_row.addWidget(self.start_time_input)

        top_row.addWidget(QLabel("Stop:"))
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setText("+5 days")
        self.stop_time_input.setMaximumWidth(100)
        top_row.addWidget(self.stop_time_input)

        self.compute_button = QPushButton("Compute")
        self.compute_button.clicked.connect(self._compute_trajectory)
        self.compute_button.setMaximumWidth(80)
        top_row.addWidget(self.compute_button)

        top_row.addStretch()

        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self._toggle_playback)
        self.play_button.setEnabled(False)
        self.play_button.setMaximumWidth(80)
        top_row.addWidget(self.play_button)

        top_row.addWidget(QLabel("Step:"))
        self.step_slider = QSlider(Qt.Horizontal)
        self.step_slider.setMinimum(1)
        self.step_slider.setMaximum(100)
        self.step_slider.setValue(10)
        self.step_slider.setEnabled(False)
        self.step_slider.setMaximumWidth(150)
        top_row.addWidget(self.step_slider)

        self.step_label = QLabel("10")
        self.step_label.setMinimumWidth(30)
        top_row.addWidget(self.step_label)
        self.step_slider.valueChanged.connect(lambda v: self.step_label.setText(str(v)))

        self.reset_button = QPushButton("⟲ Reset")
        self.reset_button.clicked.connect(self._reset_animation)
        self.reset_button.setEnabled(False)
        self.reset_button.setMaximumWidth(70)
        top_row.addWidget(self.reset_button)

        top_row.addWidget(QLabel("Time:"))
        self.current_time_label = QLabel("--")
        self.current_time_label.setMinimumWidth(150)
        top_row.addWidget(self.current_time_label)

        main_controls.addLayout(top_row)

        return main_controls

    def _setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.setInterval(100)

    def _draw_world_map(self):
        self.ax.clear()

        if self.world is not None:
            self.world.plot(ax=self.ax, color='lightgray', edgecolor='black', linewidth=0.3, rasterized=True)
        else:
            self.ax.set_facecolor('#e6f2ff')
            for lat in range(-90, 91, 30):
                self.ax.axhline(y=lat, color='gray', linewidth=0.3, alpha=0.3)
            for lon in range(-180, 181, 30):
                self.ax.axvline(x=lon, color='gray', linewidth=0.3, alpha=0.3)

        self.ax.set_xlim(-180, 180)
        self.ax.set_ylim(-90, 90)
        self.ax.set_title(f"SGP4 Propagation: {self.propagation_data['name']}")
        self.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        self.canvas.draw()

    def _compute_trajectory(self):
        start_time = self.propagation_data['epoch']
        stop_time_str = self.stop_time_input.text()

        self.trajectory = self.propagator_controller.compute_trajectory(
            self.propagation_data['tle_line1'],
            self.propagation_data['tle_line2'],
            start_time,
            stop_time_str,
            step_seconds=60
        )

        self.current_index = 0
        self.play_button.setEnabled(True)
        self.step_slider.setEnabled(True)
        self.reset_button.setEnabled(True)

        self._draw_trajectory()
        self._update_time_display()

        lon = self.trajectory['longitudes'][0]
        lat = self.trajectory['latitudes'][0]
        self.satellite_marker.set_data([lon], [lat])
        self.canvas.draw()

    def _draw_trajectory(self):
        self._draw_world_map()

        lons = self.trajectory['longitudes']
        lats = self.trajectory['latitudes']

        wrapped_lons = []
        wrapped_lats = []

        for i in range(len(lons)):
            if i > 0 and abs(lons[i] - lons[i - 1]) > 180:
                wrapped_lons.append(np.nan)
                wrapped_lats.append(np.nan)
            wrapped_lons.append(lons[i])
            wrapped_lats.append(lats[i])

        self.trajectory_line, = self.ax.plot(wrapped_lons, wrapped_lats, 'b-', linewidth=1.5, alpha=0.6,
                                             label='Trajectory')

        self.satellite_marker, = self.ax.plot([], [], 'ro', markersize=10, label='Satellite')

        self.ax.legend(loc='upper right')
        self.canvas.draw()

    def _toggle_playback(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button.setText("▶ Play")
            self.timer.stop()
        else:
            self.is_playing = True
            self.play_button.setText("⸠Pause")
            self.timer.start()

    def _reset_animation(self):
        if self.trajectory is None:
            return

        self.current_index = 0
        if self.is_playing:
            self.is_playing = False
            self.play_button.setText("▶ Play")
            self.timer.stop()

        lon = self.trajectory['longitudes'][0]
        lat = self.trajectory['latitudes'][0]
        self.satellite_marker.set_data([lon], [lat])
        self._update_time_display()
        self.canvas.draw()

    def _update_time_display(self):
        if self.trajectory is None:
            return

        current_time = self.trajectory['times'][self.current_index]
        self.current_time_label.setText(current_time.strftime('%Y-%m-%d %H:%M:%S'))

    def _update_animation(self):
        if self.trajectory is None:
            return

        step_size = self.step_slider.value()
        self.current_index += step_size

        if self.current_index >= len(self.trajectory['times']):
            self.current_index = 0

        lon = self.trajectory['longitudes'][self.current_index]
        lat = self.trajectory['latitudes'][self.current_index]

        self.satellite_marker.set_data([lon], [lat])
        self._update_time_display()
        self.canvas.draw_idle()