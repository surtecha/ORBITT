import geopandas as gpd
import os


class MapLoader:
    _instance = None
    _world_map = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MapLoader, cls).__new__(cls)
        return cls._instance

    def load_world_map(self):
        if self._world_map is None:
            shapefile_path = os.path.join('assets', 'ne_10m_land', 'ne_10m_land.shp')
            if os.path.exists(shapefile_path):
                self._world_map = gpd.read_file(shapefile_path)
                self._world_map = self._world_map.simplify(tolerance=0.01)
        return self._world_map

    def get_world_map(self):
        return self._world_map