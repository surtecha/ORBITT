import sys
from PySide6.QtWidgets import QApplication
from app.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show()
    sys.exit(app.exec())