from ui.main_window import MainWindow
from backend.controllers.tle_controller import TLEController
from backend.controllers.login_controller import LoginController


class AppController:
    def __init__(self):
        self.main_window = MainWindow()
        self.tle_controller = TLEController()
        self.login_controller = LoginController(self.main_window)

        self._connect_signals()
        self._update_login_menu()

    def _connect_signals(self):
        # TLE loading signals
        self.main_window.load_tle_requested.connect(self.tle_controller.load_tle)
        self.main_window.load_spacetrack_tle_requested.connect(self.tle_controller.load_spacetrack_tle)
        self.main_window.rename_requested.connect(self.tle_controller.rename_satellite)
        self.main_window.table_requested.connect(self.tle_controller.get_satellite_data)
        self.main_window.delete_requested.connect(self.tle_controller.delete_satellite)
        self.main_window.export_csv_requested.connect(self.tle_controller.export_csv)
        self.main_window.export_tle_requested.connect(self.tle_controller.export_tle)

        self.tle_controller.satellite_added.connect(self.main_window.add_satellite_to_sidebar)
        self.tle_controller.satellite_renamed.connect(self.main_window.update_satellite_name)
        self.tle_controller.satellite_removed.connect(self.main_window.remove_satellite)
        self.tle_controller.satellite_data_ready.connect(self.main_window.show_satellite_table)
        
        # Login signals
        self.main_window.login_action.triggered.connect(self.login_controller.handle_login_click)
        self.main_window.logout_action.triggered.connect(self.login_controller.handle_logout_click)
        self.login_controller.login_status_changed.connect(self._on_login_status_changed)
    
    def _update_login_menu(self):
        """Update login menu state based on current login status."""
        self.login_controller.update_menu_state(
            self.main_window.login_action,
            self.main_window.logout_action,
            self.main_window.insert_spacetrack
        )
    
    def _on_login_status_changed(self, logged_in):
        """Handle login status changes."""
        self._update_login_menu()

    def show(self):
        self.main_window.show()