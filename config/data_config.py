import json
import os
from pathlib import Path


class DataConfig:
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / "app_config.json"
        self.config = self.load_config()

    def load_config(self):
        default_config = {
            "data_directory": ""
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except (json.JSONDecodeError, IOError):
                return default_config
        else:
            self.save_config(default_config)
            return default_config

    def save_config(self, config=None):
        if config is None:
            config = self.config

        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.config = config
        except IOError as e:
            print(f"Error saving config: {e}")

    def get_data_directory(self):
        return self.config.get("data_directory", "")

    def set_data_directory(self, path):
        self.config["data_directory"] = path
        self.create_objects_folder(path)
        self.save_config()

    def create_objects_folder(self, base_path):
        if base_path and os.path.exists(base_path):
            objects_path = Path(base_path) / "objects"
            try:
                objects_path.mkdir(exist_ok=True)
            except OSError as e:
                print(f"Error creating objects folder: {e}")

    def get_objects_directory(self):
        data_dir = self.get_data_directory()
        if data_dir:
            return str(Path(data_dir) / "objects")
        return ""