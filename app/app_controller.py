from ui.main_window import MainWindow
from backend.controllers.tle_controller import TLEController


class AppController:
    def __init__(self):
        self.main_window = MainWindow()
        self.tle_controller = TLEController()

        self._connect_signals()

    def _connect_signals(self):
        self.main_window.load_tle_requested.connect(self.tle_controller.load_tle)
        self.main_window.rename_requested.connect(self.tle_controller.rename_satellite)
        self.main_window.table_requested.connect(self.tle_controller.get_satellite_data)
        self.main_window.delete_requested.connect(self.tle_controller.delete_satellite)

        self.tle_controller.satellite_added.connect(self.main_window.add_satellite_to_sidebar)
        self.tle_controller.satellite_renamed.connect(self.main_window.update_satellite_name)
        self.tle_controller.satellite_removed.connect(self.main_window.remove_satellite)
        self.tle_controller.satellite_data_ready.connect(self.main_window.show_satellite_table)

    def show(self):
        self.main_window.show()