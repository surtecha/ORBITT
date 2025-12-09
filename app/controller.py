from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QAction
from ui.sidebar import Sidebar
from ui.tab_manager import TabManager
from ui.dialogs.rename_dialog import RenameDialog
from backend.tle.parser import parse_tle_file
from backend.utils.file_handler import open_tle_file
from data.satellites import SatelliteData
import uuid

class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Orbital Retrieval and Behaviour Inspection Tool for TLEs")
        self.showMaximized()
        
        self.satellites = {}
        
        self._setup_ui()
        self._create_menubar()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        self.sidebar.rename_requested.connect(self.handle_rename_request)
        self.sidebar.table_requested.connect(self.handle_table_request)
        self.sidebar.delete_requested.connect(self.handle_delete_request)
        layout.addWidget(self.sidebar)
        
        self.tab_manager = TabManager()
        layout.addWidget(self.tab_manager)
    
    def _create_menubar(self):
        menubar = self.menuBar()
        
        insert_menu = menubar.addMenu("Insert")
        insert_local = QAction("Insert Local TLE", self)
        insert_local.triggered.connect(self.insert_local_tle)
        insert_menu.addAction(insert_local)
        
        insert_spacetrack = QAction("Insert from SpaceTrack", self)
        insert_menu.addAction(insert_spacetrack)
        
        login_menu = menubar.addMenu("Login")
        login_action = QAction("Login to Spacetrack", self)
        login_menu.addAction(login_action)
    
    def insert_local_tle(self):
        filepath = open_tle_file()
        if not filepath:
            return
            
        result = parse_tle_file(filepath)
        satellite_id = str(uuid.uuid4())
        
        satellite = SatelliteData(
            satellite_id=satellite_id,
            norad_id=result['norad_id'],
            name=result['norad_id'],
            dataframe=result['dataframe']
        )
        
        self.satellites[satellite_id] = satellite
        self.sidebar.add_satellite_item(satellite_id, satellite.name)
    
    def handle_rename_request(self, satellite_id):
        satellite = self.satellites.get(satellite_id)
        if not satellite:
            return
            
        dialog = RenameDialog(satellite.name, self)
        if dialog.exec():
            satellite.name = dialog.get_name()
            self.sidebar.update_satellite_name(satellite_id, satellite.name)
    
    def handle_table_request(self, satellite_id):
        satellite = self.satellites.get(satellite_id)
        if satellite:
            self.tab_manager.create_tabular_tab(satellite_id, satellite.name, satellite.dataframe)
    
    def handle_delete_request(self, satellite_id):
        if satellite_id in self.satellites:
            del self.satellites[satellite_id]
            self.sidebar.remove_satellite_item(satellite_id)
            self.tab_manager.close_tabs_for_satellite(satellite_id)