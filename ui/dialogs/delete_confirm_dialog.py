from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PySide6.QtCore import Qt


class DeleteConfirmDialog(QDialog):
    def __init__(self, object_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Deletion")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        message = QLabel(f"Are you sure you want to delete '{object_name}'?")
        layout.addWidget(message)
        
        warning = QLabel("This action cannot be undone.")
        warning.setStyleSheet("color: palette(mid);")
        layout.addWidget(warning)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
