from PySide6.QtWidgets import QToolBar, QComboBox, QLabel
from PySide6.QtCore import Signal
from config.data_config import DataConfig
from ui.components.folder_selector import FolderSelector


class ToolBar(QToolBar):
    tab_clicked = Signal(str)
    group_changed = Signal(str)
    folder_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)
        self.setFloatable(False)

        self.config_manager = DataConfig()

        self.tab_groups = {
            "Visualizer": ["Plotter", "Fetcher", "Bulk Extractor"],
            "Neural Network": ["Predictor", "Training"]
        }

        self.dropdown = None
        self.folder_label = None
        self.folder_selector = None

        self.setup_ui()

    def setup_ui(self):
        self.dropdown = QComboBox()
        self.dropdown.addItems(list(self.tab_groups.keys()))
        self.dropdown.currentTextChanged.connect(self.on_group_changed)
        self.addWidget(self.dropdown)

        self.addSeparator()

        self.folder_label = QLabel("Satellite Data Folder:")
        self.folder_selector = FolderSelector("Select the folder to store/load satellite data")
        self.folder_selector.setMaximumWidth(500)

        saved_path = self.config_manager.get_data_directory()
        if saved_path:
            self.folder_selector.path_display.setText(saved_path)

        self.folder_selector.path_display.textChanged.connect(self.on_folder_changed)

        self.addWidget(self.folder_label)
        self.addWidget(self.folder_selector)

        self.on_group_changed(self.dropdown.currentText())

    def on_group_changed(self, selection):
        self.group_changed.emit(selection)

        tabs = self.tab_groups.get(selection, [])
        if tabs:
            self.tab_clicked.emit(tabs[0])

    def on_folder_changed(self, folder_path):
        if folder_path:
            self.config_manager.set_data_directory(folder_path)
            self.folder_selected.emit(folder_path)

    def get_selected_folder(self):
        return self.folder_selector.get_path()

    def set_folder_path(self, path):
        self.folder_selector.path_display.setText(path)
        self.config_manager.set_data_directory(path)