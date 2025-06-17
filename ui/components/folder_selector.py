from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QFileDialog

class FolderSelector(QWidget):
    def __init__(self, placeholder="No folder selected", parent=None):
        super().__init__(parent)
        self.layout = None
        self.path_display = None
        self.folder_button = None
        self.setup_ui(placeholder)

    def setup_ui(self, placeholder):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.path_display = QLineEdit()
        self.path_display.setPlaceholderText(placeholder)
        self.path_display.setReadOnly(True)

        self.folder_button = QPushButton("📁")
        self.folder_button.setMaximumWidth(30)
        self.folder_button.clicked.connect(self.select_folder)

        self.layout.addWidget(self.path_display)
        self.layout.addWidget(self.folder_button)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.path_display.setText(folder_path)

    def get_path(self):
        return self.path_display.text()