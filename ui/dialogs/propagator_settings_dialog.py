from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QSlider, QGroupBox, QColorDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class PropagatorSettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Propagator Settings")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self.settings = current_settings.copy()
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
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
    
    def _create_visual_controls(self):
        group = QGroupBox("Visual Settings")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        thickness_layout = QHBoxLayout()
        thickness_layout.addWidget(QLabel("Trace Thickness:"))
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
        
        color_layout.addWidget(QLabel("Trace Color:"))
        self.trace_color_btn = QPushButton()
        self.trace_color_btn.setMaximumWidth(50)
        self.trace_color_btn.setStyleSheet(f"background-color: {self.settings['trace_color']};")
        self.trace_color_btn.clicked.connect(self._pick_trace_color)
        color_layout.addWidget(self.trace_color_btn)
        
        color_layout.addWidget(QLabel("Marker Color:"))
        self.marker_color_btn = QPushButton()
        self.marker_color_btn.setMaximumWidth(50)
        self.marker_color_btn.setStyleSheet(f"background-color: {self.settings['marker_color']};")
        self.marker_color_btn.clicked.connect(self._pick_marker_color)
        color_layout.addWidget(self.marker_color_btn)
        
        color_layout.addStretch()
        
        layout.addLayout(color_layout)
        
        group.setLayout(layout)
        return group
    
    def _pick_trace_color(self):
        current_color = QColor(self.settings['trace_color'])
        color = QColorDialog.getColor(current_color, self, "Select Trace Color")
        
        if color.isValid():
            self.settings['trace_color'] = color.name()
            self.trace_color_btn.setStyleSheet(f"background-color: {color.name()};")
    
    def _pick_marker_color(self):
        current_color = QColor(self.settings['marker_color'])
        color = QColorDialog.getColor(current_color, self, "Select Marker Color")
        
        if color.isValid():
            self.settings['marker_color'] = color.name()
            self.marker_color_btn.setStyleSheet(f"background-color: {color.name()};")
    
    def get_settings(self):
        self.settings['thickness'] = self.thickness_slider.value()
        return self.settings
