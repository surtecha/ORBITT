import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.app_controller import AppController
from backend.utils.map_loader import MapLoader

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("ORBITT")
    app.setOrganizationName("ORBITT")
    app.setWindowIcon(QIcon("assets/icon.png"))

    map_loader = MapLoader()
    map_loader.load_world_map()

    controller = AppController()
    controller.show()
    sys.exit(app.exec())