from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMenu
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

class Sidebar(QWidget):
    rename_requested = Signal(str)
    table_requested = Signal(str)
    plot_requested = Signal(str)
    propagate_requested = Signal(str)
    delete_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.satellite_labels = {}
    
    def add_satellite_item(self, satellite_id, display_name):
        label = QLabel(display_name)
        label.setCursor(Qt.PointingHandCursor)
        label.mouseDoubleClickEvent = lambda e: self.table_requested.emit(satellite_id)
        label.setContextMenuPolicy(Qt.CustomContextMenu)
        label.customContextMenuRequested.connect(lambda pos: self._show_context_menu(satellite_id))
        
        self.layout.addWidget(label)
        self.satellite_labels[satellite_id] = label
    
    def update_satellite_name(self, satellite_id, new_name):
        if satellite_id in self.satellite_labels:
            self.satellite_labels[satellite_id].setText(new_name)
    
    def remove_satellite_item(self, satellite_id):
        if satellite_id in self.satellite_labels:
            label = self.satellite_labels[satellite_id]
            self.layout.removeWidget(label)
            label.deleteLater()
            del self.satellite_labels[satellite_id]
    
    def _show_context_menu(self, satellite_id):
        menu = QMenu(self)
        actions = {
            "Rename": self.rename_requested,
            "Table": self.table_requested,
            "Plot": self.plot_requested,
            "Propagate": self.propagate_requested,
            "Delete": self.delete_requested
        }
        
        for text, signal in actions.items():
            menu.addAction(text)
        
        action = menu.exec(QCursor.pos())
        if action:
            actions[action.text()].emit(satellite_id)