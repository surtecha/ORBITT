from dataclasses import dataclass
import pandas as pd

@dataclass
class SatelliteData:
    satellite_id: str
    norad_id: str
    name: str
    dataframe: pd.DataFrame