from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from ui.sidebar import Sidebar
from ui.tab_manager import TabManager
from ui.dialogs.rename_dialog import RenameDialog
from ui.dialogs.delete_confirm_dialog import DeleteConfirmDialog
from backend.utils.file_handler import open_tle_file


class MainWindow(QMainWindow):
    load_tle_requested = Signal(str)
    rename_requested = Signal(str, str)
    table_requested = Signal(str)
    plot_requested = Signal(str)
    propagate_requested = Signal(str)
    delete_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Orbital Retrieval and Behaviour Inspection Tool for TLEs")
        self.showMaximized()

        self._setup_ui()
        self._create_menubar()
        self._connect_signals()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        self.tab_manager = TabManager()
        layout.addWidget(self.tab_manager)

    def _create_menubar(self):
        menubar = self.menuBar()

        insert_menu = menubar.addMenu("Insert")
        insert_local = QAction("Insert Local TLE", self)
        insert_local.triggered.connect(self._on_insert_local_tle)
        insert_menu.addAction(insert_local)

        insert_spacetrack = QAction("Insert from SpaceTrack", self)
        insert_menu.addAction(insert_spacetrack)

        login_menu = menubar.addMenu("Login")
        login_action = QAction("Login to Spacetrack", self)
        login_menu.addAction(login_action)

    def _connect_signals(self):
        self.sidebar.rename_requested.connect(self._on_rename_requested)
        self.sidebar.table_requested.connect(self.table_requested.emit)
        self.sidebar.plot_requested.connect(self.plot_requested.emit)
        self.sidebar.propagate_requested.connect(self.propagate_requested.emit)
        self.sidebar.delete_requested.connect(self._on_delete_requested)

    def _on_insert_local_tle(self):
        filepath = open_tle_file()
        if filepath:
            self.load_tle_requested.emit(filepath)

    def _on_rename_requested(self, satellite_id):
        current_name = self.sidebar.get_satellite_name(satellite_id)
        dialog = RenameDialog(current_name, self)
        if dialog.exec():
            new_name = dialog.get_name()
            self.rename_requested.emit(satellite_id, new_name)

    def _on_delete_requested(self, satellite_id):
        object_name = self.sidebar.get_satellite_name(satellite_id)
        dialog = DeleteConfirmDialog(object_name, self)
        if dialog.exec():
            self.delete_requested.emit(satellite_id)

    def add_satellite_to_sidebar(self, satellite):
        self.sidebar.add_satellite_item(satellite.satellite_id, satellite.name)

    def update_satellite_name(self, satellite_id, new_name):
        self.sidebar.update_satellite_name(satellite_id, new_name)
        self.tab_manager.update_tab_names(satellite_id, new_name)

    def remove_satellite(self, satellite_id):
        self.sidebar.remove_satellite_item(satellite_id)
        self.tab_manager.close_tabs_for_satellite(satellite_id)

    def show_satellite_table(self, satellite_id, name, dataframe):
        self.tab_manager.create_tabular_tab(satellite_id, name, dataframe)