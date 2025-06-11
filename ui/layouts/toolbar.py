from PySide6.QtWidgets import QToolBar, QTabWidget, QComboBox, QWidget
from PySide6.QtCore import Signal


class ToolBar(QToolBar):
    tab_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)
        self.setFloatable(False)

        # Tab definitions
        self.tab_groups = {
            "Visualizer": ["Plotter", "Fetcher", "Bulk Extractor"],
            "Neural Network": ["Predictor", "Training"]
        }

        # Setup UI components
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.addWidget(self.tab_widget)

        self.dropdown = QComboBox()
        self.dropdown.addItems(list(self.tab_groups.keys()))
        self.dropdown.currentTextChanged.connect(self.switch_tabs)
        self.addWidget(self.dropdown)

        # Initialize with first group
        self.switch_tabs(self.dropdown.currentText())

    def switch_tabs(self, selection):
        self.tab_widget.clear()
        tabs = self.tab_groups.get(selection, [])

        for tab in tabs:
            self.tab_widget.addTab(QWidget(), tab)

        # Emit signal for first tab if any tabs exist
        if tabs:
            self.tab_clicked.emit(tabs[0])

    def on_tab_changed(self, index):
        if index >= 0:
            tab_name = self.tab_widget.tabText(index)
            self.tab_clicked.emit(tab_name)