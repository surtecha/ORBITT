from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class LogViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = None
        self.log_text_area = None
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Log text area (always visible)
        self.log_text_area = QTextEdit()
        self.log_text_area.setReadOnly(True)
        self.log_text_area.setPlaceholderText("Logs will appear here...")
        self.layout.addWidget(self.log_text_area)

    def add_log(self, message):
        """Method to add log messages (for future use)"""
        self.log_text_area.append(message)

    def clear_log(self):
        """Method to clear the log (for future use)"""
        self.log_text_area.clear()