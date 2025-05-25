from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
from .topbar.topbar import TopBar
from .tle_processor.sidebar.sidebar import Sidebar
from .tle_processor.tabs.plotter import Plotter
from .tle_processor.tabs.extractor import Extractor
from .neural_network.tabs.model_architecture import ModelArchitecture
from styles.stylesheet import get_widget_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ORBITT - Orbital Retrieval and Behaviour Inspection Tool for TLEs')
        self.setGeometry(100, 100, 1400, 900)

        if os.path.exists('logo.png'):
            self.setWindowIcon(QIcon('logo.png'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.topbar = TopBar()
        main_layout.addWidget(self.topbar)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)

        self.main_content = QWidget()
        self.main_content.setStyleSheet(get_widget_style('content'))
        content_layout.addWidget(self.main_content, 1)

        main_layout.addLayout(content_layout, 1)

        self.setup_tabs()
        self.connect_signals()

        self.topbar.set_active_dropdown("Visualize")
        self.topbar.set_active_tab("Plotter")

    def setup_tabs(self):
        self.tabs = {
            'Plotter': Plotter(),
            'Extractor': Extractor(),
            'Model Architecture': ModelArchitecture()
        }

        content_layout = QVBoxLayout(self.main_content)
        content_layout.setContentsMargins(0, 0, 0, 0)


        for tab_widget in self.tabs.values():
            content_layout.addWidget(tab_widget)
            tab_widget.hide()

        if 'Plotter' in self.tabs:
            self.tabs['Plotter'].show()
        elif self.tabs:
            list(self.tabs.values())[0].show()


    def connect_signals(self):
        self.topbar.dropdown_changed.connect(self.on_dropdown_changed)
        self.topbar.tab_changed.connect(self.on_tab_changed)

    def on_dropdown_changed(self, dropdown_name):
        if dropdown_name == "Visualize":
            self.sidebar.show()
            if "Plotter" in self.tabs:
                self.topbar.set_active_tab("Plotter")
                self.on_tab_changed("Plotter")
            elif "Extractor" in self.tabs:
                 self.topbar.set_active_tab("Extractor")
                 self.on_tab_changed("Extractor")

        elif dropdown_name == "Neural Network":
            self.sidebar.hide()
            if "Model Architecture" in self.tabs:
                self.topbar.set_active_tab("Model Architecture")
                self.on_tab_changed("Model Architecture")
        else:
            self.sidebar.hide()


    def on_tab_changed(self, tab_name):
        for name, widget in self.tabs.items():
            if name == tab_name:
                widget.show()
            else:
                widget.hide()