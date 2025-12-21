from sgp4.api import Satrec, jday
from datetime import datetime, timedelta
import numpy as np
import math


def propagate_orbit(tle_line1, tle_line2, start_time, stop_time, step_seconds=60):
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    
    current_time = start_time
    times = []
    positions = []
    velocities = []
    
    while current_time <= stop_time:
        jd, fr = jday(current_time.year, current_time.month, current_time.day,
                      current_time.hour, current_time.minute, current_time.second)
        
        error_code, position, velocity = satellite.sgp4(jd, fr)
        
        if error_code == 0:
            times.append(current_time)
            positions.append(position)
            velocities.append(velocity)
        
        current_time += timedelta(seconds=step_seconds)
    
    return {
        'times': times,
        'positions': np.array(positions),
        'velocities': np.array(velocities)
    }


def get_orbital_period_minutes(tle_line1, tle_line2):
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    mean_motion = satellite.no_kozai
    period_minutes = (2 * math.pi) / mean_motion
    return period_minutes


def compute_position_at_time(tle_line1, tle_line2, target_time):
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    
    jd, fr = jday(target_time.year, target_time.month, target_time.day,
                  target_time.hour, target_time.minute, target_time.second)
    
    error_code, position, velocity = satellite.sgp4(jd, fr)
    
    if error_code == 0:
        return position, velocity
    return None, None
