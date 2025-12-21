from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMenu
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QFont, QPalette


class Sidebar(QWidget):
    rename_requested = Signal(str)
    duplicate_requested = Signal(str)
    table_requested = Signal(str)
    plot_requested = Signal(str)
    propagate_requested = Signal(str)
    ground_trace_requested = Signal(str)
    delete_requested = Signal(str)
    export_csv_requested = Signal(str)
    export_tle_requested = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(250)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        header = QLabel("Objects")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(header)

        self.satellite_labels = {}
        self.selected_id = None

    def add_satellite_item(self, satellite_id, display_name):
        label = QLabel(display_name)
        label.setFont(QFont("Arial", 13))
        label.setCursor(Qt.PointingHandCursor)
        label.setStyleSheet("padding: 8px; border-radius: 3px;")
        label.mousePressEvent = lambda e: self._on_label_clicked(e, satellite_id)
        label.mouseDoubleClickEvent = lambda e: self.table_requested.emit(satellite_id)
        label.setContextMenuPolicy(Qt.CustomContextMenu)
        label.customContextMenuRequested.connect(lambda pos: self._show_context_menu(satellite_id))

        self.layout.addWidget(label)
        self.satellite_labels[satellite_id] = label

    def _on_label_clicked(self, event, satellite_id):
        self._select_satellite(satellite_id)
        if event.button() == Qt.LeftButton and event.type() == event.Type.MouseButtonDblClick:
            self.table_requested.emit(satellite_id)

    def _select_satellite(self, satellite_id):
        palette = self.palette()
        if self.selected_id:
            self.satellite_labels[self.selected_id].setStyleSheet("padding: 8px; border-radius: 3px;")

        self.selected_id = satellite_id
        highlight_color = palette.color(QPalette.Highlight).name()
        self.satellite_labels[satellite_id].setStyleSheet(
            f"padding: 8px; border-radius: 3px; background-color: {highlight_color};"
        )

    def update_satellite_name(self, satellite_id, new_name):
        if satellite_id in self.satellite_labels:
            self.satellite_labels[satellite_id].setText(new_name)

    def remove_satellite_item(self, satellite_id):
        if satellite_id in self.satellite_labels:
            label = self.satellite_labels[satellite_id]
            self.layout.removeWidget(label)
            label.deleteLater()
            del self.satellite_labels[satellite_id]
            if self.selected_id == satellite_id:
                self.selected_id = None

    def get_satellite_name(self, satellite_id):
        if satellite_id in self.satellite_labels:
            return self.satellite_labels[satellite_id].text()
        return ""

    def _show_context_menu(self, satellite_id):
        self._select_satellite(satellite_id)
        menu = QMenu(self)
        menu.setMinimumWidth(180)
        
        menu.addAction("Table")
        menu.addAction("Plot")
        menu.addAction("Propagate")
        menu.addAction("Ground Trace")
        menu.addSeparator()
        
        menu.addAction("Rename")
        menu.addSeparator()
        
        menu.addAction("Export as CSV")
        
        export_tle_menu = menu.addMenu("Export as TLE")
        export_tle_menu.addAction("Export as .tle")
        export_tle_menu.addAction("Export as .txt")
        
        menu.addSeparator()
        
        delete_action = menu.addAction("Delete")
        font = delete_action.font()
        font.setBold(True)
        delete_action.setFont(font)
        
        action = menu.exec(QCursor.pos())
        if action:
            text = action.text()
            if text == "Export as CSV":
                self.export_csv_requested.emit(self.selected_id)
            elif text == "Export as .tle":
                self.export_tle_requested.emit(self.selected_id, ".tle")
            elif text == "Export as .txt":
                self.export_tle_requested.emit(self.selected_id, ".txt")
            else:
                action_map = {
                    "Rename": self.rename_requested,
                    "Table": self.table_requested,
                    "Plot": self.plot_requested,
                    "Propagate": self.propagate_requested,
                    "Ground Trace": self.ground_trace_requested,
                    "Delete": self.delete_requested
                }
                if text in action_map:
                    action_map[text].emit(self.selected_id)