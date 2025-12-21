from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QSlider, QGroupBox)
from PySide6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from backend.utils.map_loader import MapLoader
from ui.dialogs.ground_trace_settings_dialog import GroundTraceSettingsDialog
import numpy as np


def create_ground_trace_widget(ground_trace_data, ground_trace_controller):
    widget = GroundTraceWidget(ground_trace_data, ground_trace_controller)
    return widget


class GroundTraceWidget(QWidget):
    def __init__(self, ground_trace_data, ground_trace_controller):
        super().__init__()

        self.ground_trace_data = ground_trace_data
        self.ground_trace_controller = ground_trace_controller
        self.trajectory = None
        self.current_index = 0
        self.is_playing = False

        period_minutes = ground_trace_data['period_minutes']
        default_interval_minutes = int(period_minutes / 2)

        self.settings = {
            'interval1_minutes': default_interval_minutes,
            'interval2_minutes': default_interval_minutes,
            'segment_colors': ['#FFD700', '#FF4444', '#FFD700'],
            'marker_color': '#FF0000',
            'thickness': 1,
            'segment_visibility': [True, True, True]
        }

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
        main_controls.setSpacing(5)

        time_group = self._create_time_controls()
        main_controls.addWidget(time_group)

        playback_group = self._create_playback_controls()
        main_controls.addWidget(playback_group)

        return main_controls

    def _create_time_controls(self):
        group = QGroupBox("Time Configuration")
        layout = QHBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(QLabel("Start:"))
        self.start_time_input = QLineEdit()
        epoch = self.ground_trace_data['epoch']
        self.start_time_input.setText(epoch.strftime('%Y-%m-%d %H:%M:%S'))
        self.start_time_input.setMaximumWidth(150)
        layout.addWidget(self.start_time_input)

        layout.addWidget(QLabel("Stop:"))
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setMaximumWidth(150)
        layout.addWidget(self.stop_time_input)

        self.compute_button = QPushButton("Compute")
        self.compute_button.clicked.connect(self._compute_trajectory)
        self.compute_button.setMaximumWidth(80)
        layout.addWidget(self.compute_button)

        layout.addWidget(QLabel("Current Time:"))
        self.current_time_input = QLineEdit("--")
        self.current_time_input.setMaximumWidth(150)
        self.current_time_input.setReadOnly(True)
        self.current_time_input.returnPressed.connect(self._on_time_input_changed)
        layout.addWidget(self.current_time_input)

        layout.addStretch()

        group.setLayout(layout)
        return group

    def _create_playback_controls(self):
        group = QGroupBox("Playback Controls")
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self._toggle_playback)
        self.play_button.setEnabled(False)
        self.play_button.setMaximumWidth(80)
        layout.addWidget(self.play_button)

        layout.addWidget(QLabel("Step:"))
        self.step_slider = QSlider(Qt.Horizontal)
        self.step_slider.setMinimum(1)
        self.step_slider.setMaximum(100)
        self.step_slider.setValue(10)
        self.step_slider.setEnabled(False)
        self.step_slider.setMaximumWidth(150)
        layout.addWidget(self.step_slider)

        self.step_label = QLabel("10")
        self.step_label.setMinimumWidth(30)
        layout.addWidget(self.step_label)
        self.step_slider.valueChanged.connect(lambda v: self.step_label.setText(str(v)))

        self.reset_button = QPushButton("⟲ Reset")
        self.reset_button.clicked.connect(self._reset_animation)
        self.reset_button.setEnabled(False)
        self.reset_button.setMaximumWidth(70)
        layout.addWidget(self.reset_button)

        self.settings_button = QPushButton("⚙ Settings")
        self.settings_button.clicked.connect(self._open_settings)
        self.settings_button.setMaximumWidth(90)
        layout.addWidget(self.settings_button)

        layout.addStretch()

        group.setLayout(layout)
        return group

    def _setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.setInterval(100)

    def _draw_world_map(self):
        self.ax.clear()

        if self.world is not None:
            self.world.plot(ax=self.ax, color='#4a4a4a', edgecolor='black', linewidth=0.3, rasterized=True)
        
        self.ax.set_facecolor('#2c5f8d')
        for lat in range(-90, 91, 30):
            self.ax.axhline(y=lat, color='gray', linewidth=0.3, alpha=0.3)
        for lon in range(-180, 181, 30):
            self.ax.axvline(x=lon, color='gray', linewidth=0.3, alpha=0.3)

        self.ax.set_xlim(-180, 180)
        self.ax.set_ylim(-90, 90)
        self.ax.set_title(f"Ground Trace: {self.ground_trace_data['name']}")
        self.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        self.canvas.draw()

    def _open_settings(self):
        dialog = GroundTraceSettingsDialog(self.settings, self)
        if dialog.exec():
            self.settings = dialog.get_settings()
            if self.trajectory:
                self._draw_trajectory()
                lon = self.trajectory['longitudes'][self.current_index]
                lat = self.trajectory['latitudes'][self.current_index]
                self.satellite_marker.set_data([lon], [lat])
                self.canvas.draw()

    def _compute_trajectory(self):
        start_time_str = self.start_time_input.text()
        stop_time_str = self.stop_time_input.text()

        start_time = self.ground_trace_controller.parse_time_input(start_time_str)
        stop_time = self.ground_trace_controller.parse_time_input(stop_time_str)

        if not start_time or not stop_time:
            return

        interval1_minutes = self.settings['interval1_minutes']
        interval2_minutes = self.settings['interval2_minutes']

        self.trajectory = self.ground_trace_controller.compute_ground_trace(
            self.ground_trace_data['tle_line1'],
            self.ground_trace_data['tle_line2'],
            start_time,
            stop_time,
            interval1_minutes,
            interval2_minutes,
            step_seconds=60
        )

        self.current_index = self.trajectory['midpoint_index']
        self.play_button.setEnabled(True)
        self.step_slider.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.current_time_input.setReadOnly(False)

        self._draw_trajectory()
        self._update_time_display()

        lon = self.trajectory['longitudes'][self.current_index]
        lat = self.trajectory['latitudes'][self.current_index]
        self.satellite_marker.set_data([lon], [lat])
        self.canvas.draw()

    def _draw_trajectory(self):
        self._draw_world_map()

        lons = self.trajectory['longitudes']
        lats = self.trajectory['latitudes']
        segments = self.trajectory['segments']

        from matplotlib.collections import LineCollection

        points = []
        colors = []
        
        for i in range(len(lons) - 1):
            if abs(lons[i+1] - lons[i]) > 180:
                continue
            
            seg_idx = segments[i]
            if not self.settings['segment_visibility'][seg_idx]:
                continue
            
            points.append([(lons[i], lats[i]), (lons[i+1], lats[i+1])])
            colors.append(self.settings['segment_colors'][seg_idx])
        
        if points:
            lc = LineCollection(points, colors=colors, linewidths=self.settings['thickness'], alpha=0.7)
            self.ax.add_collection(lc)

        self.satellite_marker, = self.ax.plot([], [], 'o', 
                                              color=self.settings['marker_color'], 
                                              markersize=10)
        self.canvas.draw()

    def _toggle_playback(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button.setText("▶ Play")
            self.timer.stop()
            self.current_time_input.setReadOnly(False)
        else:
            self.is_playing = True
            self.play_button.setText("⏸ Pause")
            self.timer.start()
            self.current_time_input.setReadOnly(True)

    def _reset_animation(self):
        if self.trajectory is None:
            return

        self.current_index = self.trajectory['midpoint_index']
        if self.is_playing:
            self.is_playing = False
            self.play_button.setText("▶ Play")
            self.timer.stop()
            self.current_time_input.setReadOnly(False)

        lon = self.trajectory['longitudes'][self.current_index]
        lat = self.trajectory['latitudes'][self.current_index]
        self.satellite_marker.set_data([lon], [lat])
        self._update_time_display()
        self.canvas.draw()

    def _update_time_display(self):
        if self.trajectory is None:
            return

        current_time = self.trajectory['times'][self.current_index]
        self.current_time_input.setText(current_time.strftime('%Y-%m-%d %H:%M:%S'))

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

    def _on_time_input_changed(self):
        if self.trajectory is None or self.is_playing:
            return

        time_str = self.current_time_input.text()
        target_time = self.ground_trace_controller.parse_time_input(time_str)

        if target_time:
            new_index = self.ground_trace_controller.find_time_index(
                self.trajectory['times'], 
                target_time
            )
            self.current_index = new_index
            
            lon = self.trajectory['longitudes'][self.current_index]
            lat = self.trajectory['latitudes'][self.current_index]
            self.satellite_marker.set_data([lon], [lat])
            self._update_time_display()
            self.canvas.draw()
