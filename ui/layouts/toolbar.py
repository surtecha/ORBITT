from PySide6.QtWidgets import QToolBar, QComboBox, QLabel
from PySide6.QtCore import Signal


class ToolBar(QToolBar):
    tab_clicked = Signal(str)
    group_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)
        self.setFloatable(False)

        self.tab_groups = {
            "Visualizer": ["Plotter", "Fetcher", "Bulk Extractor"],
            "Neural Network": ["Predictor", "Training"]
        }

        self.setup_ui()

    def setup_ui(self):
        self.dropdown = QComboBox()
        self.dropdown.addItems(list(self.tab_groups.keys()))
        self.dropdown.currentTextChanged.connect(self.on_group_changed)
        self.addWidget(self.dropdown)

        self.on_group_changed(self.dropdown.currentText())

    def on_group_changed(self, selection):
        self.group_changed.emit(selection)
        tabs = self.tab_groups.get(selection, [])
        if tabs:
            self.tab_clicked.emit(tabs[0])