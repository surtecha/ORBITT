import sys
from PySide6.QtWidgets import QApplication
from app.app_controller import AppController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()
    sys.exit(app.exec())