from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget
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

        # Main area (central widget)
        self.main_area = QWidget()
        self.setCentralWidget(self.main_area)

        # Sidebar as dock widget
        self.sidebar = SideBar(self)
        self.sidebar_dock = QDockWidget("", self)
        self.sidebar_dock.setWidget(self.sidebar)
        self.sidebar_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.sidebar_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_dock)

        # MenuBar
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        # Toolbar
        self.toolbar = ToolBar(self)
        self.addToolBar(self.toolbar)

        # Connect toolbar signal to sidebar update
        self.toolbar.tab_clicked.connect(self.update_sidebar_for_tab)

        # Initialize with default tab
        self.update_sidebar_for_tab("Plotter")

    def update_sidebar_for_tab(self, tab_name):
        tab_module = TAB_WIDGET_MAP.get(tab_name)
        if tab_module:
            primary, secondary = tab_module.get_sidebar_widgets()
            self.sidebar.set_primary_widgets(primary)
            self.sidebar.set_secondary_widgets(secondary)