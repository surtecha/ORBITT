from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from ui.sidebar import Sidebar
from ui.tab_manager import TabManager
from ui.dialogs.rename_dialog import RenameDialog
from ui.dialogs.delete_confirm_dialog import DeleteConfirmDialog
from ui.dialogs.spacetrack_tle_dialog import SpaceTrackTLEDialog
from backend.utils.file_handler import open_tle_file


class MainWindow(QMainWindow):
    load_tle_requested = Signal(str)
    load_spacetrack_tle_requested = Signal(str)
    rename_requested = Signal(str, str)
    table_requested = Signal(str)
    plot_requested = Signal(str)
    propagate_requested = Signal(str)
    delete_requested = Signal(str)
    export_csv_requested = Signal(str)
    export_tle_requested = Signal(str, str)

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

        # Insert menu
        insert_menu = menubar.addMenu("Insert")
        insert_local = QAction("Insert Local TLE", self)
        insert_local.triggered.connect(self._on_insert_local_tle)
        insert_menu.addAction(insert_local)

        self.insert_spacetrack = QAction("Insert from SpaceTrack", self)
        self.insert_spacetrack.triggered.connect(self._on_insert_spacetrack_tle)
        self.insert_spacetrack.setEnabled(False)  # Disabled until logged in
        insert_menu.addAction(self.insert_spacetrack)

        # Login menu
        login_menu = menubar.addMenu("Login")
        self.login_action = QAction("Login to Space-Track", self)
        login_menu.addAction(self.login_action)
        
        self.logout_action = QAction("Logout", self)
        self.logout_action.setVisible(False)
        login_menu.addAction(self.logout_action)

    def _connect_signals(self):
        self.sidebar.rename_requested.connect(self._on_rename_requested)
        self.sidebar.table_requested.connect(self.table_requested.emit)
        self.sidebar.plot_requested.connect(self.plot_requested.emit)
        self.sidebar.propagate_requested.connect(self.propagate_requested.emit)
        self.sidebar.delete_requested.connect(self._on_delete_requested)
        self.sidebar.export_csv_requested.connect(self.export_csv_requested.emit)
        self.sidebar.export_tle_requested.connect(self.export_tle_requested.emit)

    def _on_insert_local_tle(self):
        filepath = open_tle_file()
        if filepath:
            self.load_tle_requested.emit(filepath)
    
    def _on_insert_spacetrack_tle(self):
        dialog = SpaceTrackTLEDialog(self)
        if dialog.exec():
            tle_data = dialog.get_tle_data()
            if tle_data:
                self.load_spacetrack_tle_requested.emit(tle_data)

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
    
    def show_satellite_plot(self, satellite_id, name, dataframe):
        self.tab_manager.create_plot_tab(satellite_id, name, dataframe)
    
    def show_satellite_propagator(self, satellite_id, name, propagation_data, propagator_controller):
        self.tab_manager.create_propagator_tab(satellite_id, name, propagation_data, propagator_controller)
    
    def update_login_menu_state(self, login_action, logout_action, spacetrack_insert_action):
        self.login_action = login_action
        self.logout_action = logout_action
        self.insert_spacetrack = spacetrack_insert_action