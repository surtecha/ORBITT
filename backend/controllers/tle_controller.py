from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from backend.tle.parser import parse_tle_file
from data.satellite import SatelliteData
import uuid


class TLEController(QObject):
    satellite_added = Signal(object)
    satellite_renamed = Signal(str, str)
    satellite_removed = Signal(str)
    satellite_data_ready = Signal(str, str, object)
    satellite_plot_ready = Signal(str, str, object)

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
            dataframe=result['dataframe'],
            tle_lines=result['tle_lines']
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
    
    def get_satellite_plot_data(self, satellite_id):
        if satellite_id in self.satellites:
            satellite = self.satellites[satellite_id]
            self.satellite_plot_ready.emit(satellite_id, satellite.name, satellite.dataframe)
    
    def load_spacetrack_tle(self, tle_data):
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(tle_data)
            temp_filepath = temp_file.name
        
        try:
            lines = tle_data.strip().split('\n')
            norad_groups = {}
            
            for i in range(0, len(lines), 2):
                if i + 1 >= len(lines):
                    break
                
                line1 = lines[i][:69]
                line2 = lines[i + 1][:69]
                
                norad_id_raw = line1[2:7].strip()
                norad_id = str(int(norad_id_raw))
                
                if norad_id not in norad_groups:
                    norad_groups[norad_id] = []
                norad_groups[norad_id].append((line1, line2))
            
            for norad_id, tle_lines in norad_groups.items():
                tle_text = '\n'.join([f"{l1}\n{l2}" for l1, l2 in tle_lines])
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as obj_file:
                    obj_file.write(tle_text)
                    obj_filepath = obj_file.name
                
                try:
                    result = parse_tle_file(obj_filepath)
                    satellite_id = str(uuid.uuid4())

                    satellite = SatelliteData(
                        satellite_id=satellite_id,
                        norad_id=norad_id,
                        name=norad_id,
                        dataframe=result['dataframe'],
                        tle_lines=result['tle_lines']
                    )

                    self.satellites[satellite_id] = satellite
                    self.satellite_added.emit(satellite)
                finally:
                    if os.path.exists(obj_filepath):
                        os.remove(obj_filepath)
        finally:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
    
    def export_csv(self, satellite_id):
        if satellite_id not in self.satellites:
            return
        
        satellite = self.satellites[satellite_id]
        filepath, _ = QFileDialog.getSaveFileName(
            None,
            "Export as CSV",
            f"{satellite.name}.csv",
            "CSV Files (*.csv)"
        )
        
        if not filepath:
            return
        
        satellite.dataframe.to_csv(filepath, index=False)
    
    def export_tle(self, satellite_id, extension):
        if satellite_id not in self.satellites:
            return
        
        satellite = self.satellites[satellite_id]
        if not satellite.tle_lines:
            return
        
        filter_str = f"TLE Files (*{extension})"
        filepath, _ = QFileDialog.getSaveFileName(
            None,
            f"Export as TLE ({extension})",
            f"{satellite.name}{extension}",
            filter_str
        )
        
        if not filepath:
            return
        
        with open(filepath, 'w') as f:
            for line1, line2 in satellite.tle_lines:
                f.write(f"{line1}\n{line2}\n")