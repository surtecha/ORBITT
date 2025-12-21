from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QSlider, QSpinBox, QCheckBox, QColorDialog, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class GroundTraceSettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ground Trace Settings")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.settings = current_settings.copy()
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        interval_group = self._create_interval_controls()
        layout.addWidget(interval_group)
        
        visual_group = self._create_visual_controls()
        layout.addWidget(visual_group)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def _create_interval_controls(self):
        group = QGroupBox("Trace Intervals")
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Interval 1:"))
        self.interval1_minutes = QSpinBox()
        self.interval1_minutes.setRange(0, 1440)
        self.interval1_minutes.setValue(self.settings['interval1_minutes'])
        self.interval1_minutes.setSuffix(" min")
        self.interval1_minutes.setMaximumWidth(100)
        layout.addWidget(self.interval1_minutes)
        
        layout.addWidget(QLabel("Interval 2:"))
        self.interval2_minutes = QSpinBox()
        self.interval2_minutes.setRange(0, 1440)
        self.interval2_minutes.setValue(self.settings['interval2_minutes'])
        self.interval2_minutes.setSuffix(" min")
        self.interval2_minutes.setMaximumWidth(100)
        layout.addWidget(self.interval2_minutes)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def _create_visual_controls(self):
        group = QGroupBox("Visual Settings")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        thickness_layout = QHBoxLayout()
        thickness_layout.addWidget(QLabel("Thickness:"))
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(5)
        self.thickness_slider.setValue(self.settings['thickness'])
        self.thickness_slider.setMaximumWidth(150)
        thickness_layout.addWidget(self.thickness_slider)
        
        self.thickness_label = QLabel(str(self.settings['thickness']))
        self.thickness_label.setMinimumWidth(20)
        thickness_layout.addWidget(self.thickness_label)
        self.thickness_slider.valueChanged.connect(lambda v: self.thickness_label.setText(str(v)))
        thickness_layout.addStretch()
        
        layout.addLayout(thickness_layout)
        
        color_layout = QHBoxLayout()
        
        self.start_trace_check = QCheckBox("Start Trace")
        self.start_trace_check.setChecked(self.settings['segment_visibility'][0])
        color_layout.addWidget(self.start_trace_check)
        
        self.start_trace_color_btn = QPushButton()
        self.start_trace_color_btn.setMaximumWidth(30)
        self.start_trace_color_btn.setStyleSheet(f"background-color: {self.settings['segment_colors'][0]};")
        self.start_trace_color_btn.clicked.connect(lambda: self._pick_color(0))
        color_layout.addWidget(self.start_trace_color_btn)
        
        self.red_trace_check = QCheckBox("Red Trace")
        self.red_trace_check.setChecked(self.settings['segment_visibility'][1])
        color_layout.addWidget(self.red_trace_check)
        
        self.red_trace_color_btn = QPushButton()
        self.red_trace_color_btn.setMaximumWidth(30)
        self.red_trace_color_btn.setStyleSheet(f"background-color: {self.settings['segment_colors'][1]};")
        self.red_trace_color_btn.clicked.connect(lambda: self._pick_color(1))
        color_layout.addWidget(self.red_trace_color_btn)
        
        self.end_trace_check = QCheckBox("End Trace")
        self.end_trace_check.setChecked(self.settings['segment_visibility'][2])
        color_layout.addWidget(self.end_trace_check)
        
        self.end_trace_color_btn = QPushButton()
        self.end_trace_color_btn.setMaximumWidth(30)
        self.end_trace_color_btn.setStyleSheet(f"background-color: {self.settings['segment_colors'][2]};")
        self.end_trace_color_btn.clicked.connect(lambda: self._pick_color(2))
        color_layout.addWidget(self.end_trace_color_btn)
        
        color_layout.addStretch()
        
        layout.addLayout(color_layout)
        
        marker_layout = QHBoxLayout()
        marker_layout.addWidget(QLabel("Marker Color:"))
        self.marker_color_btn = QPushButton()
        self.marker_color_btn.setMaximumWidth(50)
        self.marker_color_btn.setStyleSheet(f"background-color: {self.settings['marker_color']};")
        self.marker_color_btn.clicked.connect(self._pick_marker_color)
        marker_layout.addWidget(self.marker_color_btn)
        marker_layout.addStretch()
        
        layout.addLayout(marker_layout)
        
        group.setLayout(layout)
        return group
    
    def _pick_color(self, segment_idx):
        current_color = QColor(self.settings['segment_colors'][segment_idx])
        color = QColorDialog.getColor(current_color, self, f"Select Color for Segment {segment_idx + 1}")
        
        if color.isValid():
            self.settings['segment_colors'][segment_idx] = color.name()
            buttons = [self.start_trace_color_btn, self.red_trace_color_btn, self.end_trace_color_btn]
            buttons[segment_idx].setStyleSheet(f"background-color: {color.name()};")
    
    def _pick_marker_color(self):
        current_color = QColor(self.settings['marker_color'])
        color = QColorDialog.getColor(current_color, self, "Select Marker Color")
        
        if color.isValid():
            self.settings['marker_color'] = color.name()
            self.marker_color_btn.setStyleSheet(f"background-color: {color.name()};")
    
    def get_settings(self):
        self.settings['interval1_minutes'] = self.interval1_minutes.value()
        self.settings['interval2_minutes'] = self.interval2_minutes.value()
        self.settings['thickness'] = self.thickness_slider.value()
        self.settings['segment_visibility'] = [
            self.start_trace_check.isChecked(),
            self.red_trace_check.isChecked(),
            self.end_trace_check.isChecked()
        ]
        return self.settings
