from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QTabWidget
from PySide6.QtCore import Signal, Qt

from ui.layouts.toolbar import ToolBar
from ui.layouts.sidebar import SideBar
from ui.layouts.menubar import MenuBar
from ui.tabs import plotter, fetcher, bulk_extractor, predictor, training

TAB_WIDGET_MAP = {
    "Plotter": plotter,
    "Fetcher": fetcher,
    "Bulk Extractor": bulk_extractor,
    "Predictor": predictor,
    "Training": training,
}


class MainWindow(QMainWindow):
    tab_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORBITT")
        self.setGeometry(0, 0, 1920, 1080)

        self.setup_ui()
        self.connect_signals()
        self.initialize_default_tab()

    def setup_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.main_layout.addWidget(self.tab_widget)

        self.setup_sidebar()
        self.setup_menubar()
        self.setup_toolbar()

    def setup_sidebar(self):
        self.sidebar = SideBar(self)
        self.sidebar_dock = QDockWidget("Controls", self)
        self.sidebar_dock.setWidget(self.sidebar)
        self.sidebar_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.sidebar_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_dock)

    def setup_menubar(self):
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

    def setup_toolbar(self):
        self.toolbar = ToolBar(self)
        self.addToolBar(self.toolbar)

    def connect_signals(self):
        self.toolbar.tab_clicked.connect(self.handle_tab_change)
        self.toolbar.group_changed.connect(self.update_tabs)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def initialize_default_tab(self):
        self.update_tabs("Visualizer")

    def update_tabs(self, group_name):
        self.tab_widget.clear()

        tab_groups = {
            "Visualizer": ["Plotter", "Fetcher", "Bulk Extractor"],
            "Neural Network": ["Predictor", "Training"]
        }

        tabs = tab_groups.get(group_name, [])

        for tab_name in tabs:
            tab_content = QWidget()
            self.tab_widget.addTab(tab_content, tab_name)

        if tabs:
            self.tab_widget.setCurrentIndex(0)
            self.handle_tab_change(tabs[0])

    def handle_tab_change(self, tab_name):
        self.update_sidebar_for_tab(tab_name)

    def on_tab_changed(self, index):
        if index >= 0:
            tab_name = self.tab_widget.tabText(index)
            self.update_sidebar_for_tab(tab_name)

    def update_sidebar_for_tab(self, tab_name):
        tab_module = TAB_WIDGET_MAP.get(tab_name)
        if tab_module:
            primary, secondary = tab_module.get_sidebar_widgets()
            self.sidebar.set_primary_widgets(primary)
            self.sidebar.set_secondary_widgets(secondary)