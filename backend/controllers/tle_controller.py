from PySide6.QtCore import QObject, Signal
from backend.tle.parser import parse_tle_file
from data.satellite import SatelliteData
import uuid


class TLEController(QObject):
    satellite_added = Signal(object)
    satellite_renamed = Signal(str, str)
    satellite_removed = Signal(str)
    satellite_data_ready = Signal(str, str, object)

    def __init__(self):
        super().__init__()
        self.satellites = {}

    def load_tle(self, filepath):
        result = parse_tle_file(filepath)
        satellite_id = str(uuid.uuid4())

        satellite = SatelliteData(
            satellite_id=satellite_id,
            norad_id=result['norad_id'],
            name=result['norad_id'],
            dataframe=result['dataframe']
        )

        self.satellites[satellite_id] = satellite
        self.satellite_added.emit(satellite)

    def rename_satellite(self, satellite_id, new_name):
        if satellite_id in self.satellites:
            self.satellites[satellite_id].name = new_name
            self.satellite_renamed.emit(satellite_id, new_name)

    def delete_satellite(self, satellite_id):
        if satellite_id in self.satellites:
            del self.satellites[satellite_id]
            self.satellite_removed.emit(satellite_id)

    def get_satellite_data(self, satellite_id):
        if satellite_id in self.satellites:
            satellite = self.satellites[satellite_id]
            self.satellite_data_ready.emit(satellite_id, satellite.name, satellite.dataframe)