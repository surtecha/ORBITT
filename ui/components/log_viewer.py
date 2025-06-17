from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QFont
from datetime import datetime

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

        self.log_text_area = QTextEdit()
        self.log_text_area.setReadOnly(True)
        self.log_text_area.setPlaceholderText("Processing logs will appear here...")

        font = QFont()
        font.setPointSize(12)
        self.log_text_area.setFont(font)

        self.log_text_area.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 8px;
                selection-background-color: #264f78;
            }
        """)

        self.layout.addWidget(self.log_text_area)

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")

        if message.startswith("🚀"):
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #81c784;'>{message}</span>"
        elif message.startswith("📂"):
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #ffb74d;'>{message}</span>"
        elif message.startswith("🔄"):
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #ba68c8;'>{message}</span>"
        elif message.startswith("📊"):
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #64b5f6;'>{message}</span>"
        elif message.startswith("✅") or "success" in message.lower():
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #81c784;'>{message}</span>"
        elif message.startswith("🎉"):
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #4db6ac; font-weight: bold;'>{message}</span>"
        elif message.startswith("❌") or message.startswith(
                "⚠️") or "failed" in message.lower() or "error" in message.lower():
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #e57373;'>{message}</span>"
        elif message.startswith("  └─"):
            if "✅" in message:
                formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #81c784;'>{message}</span>"
            else:
                formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #e57373;'>{message}</span>"
        else:
            formatted_message = f"<span style='color: #4fc3f7; font-weight: bold;'>[{timestamp}]</span> <span style='color: #d4d4d4;'>{message}</span>"

        self.log_text_area.append(formatted_message)

        scrollbar = self.log_text_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self):
        self.log_text_area.clear()