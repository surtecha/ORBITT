from skyfield.api import EarthSatellite, load, wgs84
import numpy as np


def convert_trajectory(times, tle_line1, tle_line2):
    ts = load.timescale()
    satellite = EarthSatellite(tle_line1, tle_line2, ts=ts)
    
    latitudes = []
    longitudes = []
    altitudes = []
    
    for time in times:
        t = ts.utc(time.year, time.month, time.day, time.hour, time.minute, time.second)
        geocentric = satellite.at(t)
        subpoint = wgs84.subpoint(geocentric)
        
        latitudes.append(subpoint.latitude.degrees)
        longitudes.append(subpoint.longitude.degrees)
        altitudes.append(subpoint.elevation.km)
    
    return np.array(latitudes), np.array(longitudes), np.array(altitudes)
