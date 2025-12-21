from PySide6.QtCore import QObject, Signal
from backend.propagator.sgp4_propagator import propagate_orbit, get_orbital_period_minutes
from backend.propagator.coordinate_converter import convert_trajectory
from datetime import datetime, timedelta


class GroundTraceController(QObject):
    ground_trace_data_ready = Signal(str, str, object)
    
    def __init__(self, tle_controller):
        super().__init__()
        self.tle_controller = tle_controller
    
    def initiate_ground_trace(self, satellite_id):
        if satellite_id not in self.tle_controller.satellites:
            return
        
        satellite = self.tle_controller.satellites[satellite_id]
        
        if not satellite.tle_lines or len(satellite.tle_lines) == 0:
            return
        
        latest_tle = satellite.tle_lines[-1]
        tle_line1, tle_line2 = latest_tle
        
        latest_epoch = satellite.dataframe['time'].iloc[-1]
        
        period_minutes = get_orbital_period_minutes(tle_line1, tle_line2)
        
        ground_trace_data = {
            'tle_line1': tle_line1,
            'tle_line2': tle_line2,
            'epoch': latest_epoch,
            'satellite_id': satellite_id,
            'name': satellite.name,
            'period_minutes': period_minutes
        }
        
        self.ground_trace_data_ready.emit(satellite_id, satellite.name, ground_trace_data)
    
    def compute_ground_trace(self, tle_line1, tle_line2, start_time, stop_time, 
                            interval1_minutes, interval2_minutes, step_seconds=60):
        
        result = propagate_orbit(tle_line1, tle_line2, start_time, stop_time, step_seconds)
        
        latitudes, longitudes, altitudes = convert_trajectory(
            result['times'],
            tle_line1,
            tle_line2
        )
        
        midpoint_time = start_time + (stop_time - start_time) / 2
        
        interval1_delta = timedelta(minutes=interval1_minutes)
        interval2_delta = timedelta(minutes=interval2_minutes)
        
        segment1_end = midpoint_time - interval1_delta
        segment2_end = midpoint_time + interval2_delta
        
        segments = self._categorize_segments(
            result['times'], 
            segment1_end, 
            segment2_end
        )
        
        midpoint_index = self._find_closest_time_index(result['times'], midpoint_time)
        
        return {
            'times': result['times'],
            'latitudes': latitudes,
            'longitudes': longitudes,
            'altitudes': altitudes,
            'segments': segments,
            'midpoint_index': midpoint_index,
            'midpoint_time': midpoint_time
        }
    
    def _categorize_segments(self, times, segment1_end, segment2_end):
        segments = []
        for time in times:
            if time < segment1_end:
                segments.append(0)
            elif time <= segment2_end:
                segments.append(1)
            else:
                segments.append(2)
        return segments
    
    def _find_closest_time_index(self, times, target_time):
        min_diff = None
        closest_index = 0
        
        for i, time in enumerate(times):
            diff = abs((time - target_time).total_seconds())
            if min_diff is None or diff < min_diff:
                min_diff = diff
                closest_index = i
        
        return closest_index
    
    def parse_time_input(self, time_str):
        time_str = time_str.strip()
        
        try:
            return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
        
        try:
            return datetime.strptime(time_str, '%Y-%m-%d')
        except ValueError:
            pass
        
        return None
    
    def find_time_index(self, times, target_time):
        return self._find_closest_time_index(times, target_time)
