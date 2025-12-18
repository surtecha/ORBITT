from PySide6.QtCore import QObject, Signal
from backend.propagator.sgp4_propagator import propagate_orbit
from backend.propagator.coordinate_converter import convert_trajectory
from datetime import datetime, timedelta
import re


class PropagatorController(QObject):
    propagation_data_ready = Signal(str, str, object)
    
    def __init__(self, tle_controller):
        super().__init__()
        self.tle_controller = tle_controller
    
    def propagate_satellite(self, satellite_id):
        if satellite_id not in self.tle_controller.satellites:
            return
        
        satellite = self.tle_controller.satellites[satellite_id]
        
        if not satellite.tle_lines or len(satellite.tle_lines) == 0:
            return
        
        latest_tle = satellite.tle_lines[-1]
        tle_line1, tle_line2 = latest_tle
        
        latest_epoch = satellite.dataframe['time'].iloc[-1]
        
        propagation_data = {
            'tle_line1': tle_line1,
            'tle_line2': tle_line2,
            'epoch': latest_epoch,
            'satellite_id': satellite_id,
            'name': satellite.name
        }
        
        self.propagation_data_ready.emit(satellite_id, satellite.name, propagation_data)
    
    def compute_trajectory(self, tle_line1, tle_line2, start_time, stop_time_str, step_seconds=60):
        stop_time = self._parse_stop_time(start_time, stop_time_str)
        
        result = propagate_orbit(tle_line1, tle_line2, start_time, stop_time, step_seconds)
        
        latitudes, longitudes, altitudes = convert_trajectory(
            result['times'],
            tle_line1,
            tle_line2
        )
        
        return {
            'times': result['times'],
            'latitudes': latitudes,
            'longitudes': longitudes,
            'altitudes': altitudes
        }
    
    def _parse_stop_time(self, start_time, stop_time_str):
        stop_time_str = stop_time_str.strip()
        
        match = re.match(r'\+\s*(\d+)\s*days?', stop_time_str, re.IGNORECASE)
        if match:
            days = int(match.group(1))
            return start_time + timedelta(days=days)
        
        try:
            return datetime.strptime(stop_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
        
        try:
            return datetime.strptime(stop_time_str, '%Y-%m-%d')
        except ValueError:
            pass
        
        return start_time + timedelta(days=5)
