from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QScrollArea
from PySide6.QtCore import Signal
from ui.components.folder_selector import FolderSelector
import os


class InputFolderSelector(QWidget):
    files_selected = Signal(list)

    def __init__(self, placeholder="No folder selected", parent=None):
        super().__init__(parent)
        self.folder_selector = FolderSelector(placeholder)
        self.select_all_checkbox = QCheckBox("Select All")
        self.file_checkboxes = []
        self.scroll_area = QScrollArea()
        self.file_widget = QWidget()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.folder_selector)
        layout.addWidget(self.select_all_checkbox)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        self.folder_selector.path_display.textChanged.connect(self.load_txt_files)
        self.select_all_checkbox.toggled.connect(self.toggle_all_files)

        self.scroll_area.setWidget(self.file_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)
        self.scroll_area.setMaximumHeight(300)

    def load_txt_files(self, folder_path):
        if self.file_widget.layout():
            for i in reversed(range(self.file_widget.layout().count())):
                self.file_widget.layout().itemAt(i).widget().deleteLater()

        self.file_checkboxes.clear()

        if not folder_path or not os.path.exists(folder_path):
            return

        txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

        file_layout = QVBoxLayout()
        file_layout.setContentsMargins(5, 5, 5, 5)
        file_layout.setSpacing(2)
        for txt_file in txt_files:
            checkbox = QCheckBox(txt_file)
            checkbox.toggled.connect(self.on_file_checkbox_toggled)
            checkbox.setSizePolicy(checkbox.sizePolicy().horizontalPolicy(), checkbox.sizePolicy().verticalPolicy())
            self.file_checkboxes.append(checkbox)
            file_layout.addWidget(checkbox)

        self.file_widget.setLayout(file_layout)
        self.select_all_checkbox.setEnabled(bool(txt_files))

    def toggle_all_files(self, checked):
        for checkbox in self.file_checkboxes:
            checkbox.setChecked(checked)

    def on_file_checkbox_toggled(self):
        checked_count = sum(1 for cb in self.file_checkboxes if cb.isChecked())
        total_count = len(self.file_checkboxes)

        self.select_all_checkbox.blockSignals(True)
        if checked_count == total_count:
            self.select_all_checkbox.setChecked(True)
        else:
            self.select_all_checkbox.setChecked(False)
        self.select_all_checkbox.blockSignals(False)

        self.emit_selected_files()

    def emit_selected_files(self):
        selected_files = [cb.text() for cb in self.file_checkboxes if cb.isChecked()]
        self.files_selected.emit(selected_files)

    def get_selected_files(self):
        return [cb.text() for cb in self.file_checkboxes if cb.isChecked()]

    def get_folder_path(self):
        return self.folder_selector.get_path()