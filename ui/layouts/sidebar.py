from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame


class SideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(200)
        self.setMinimumWidth(150)
        self.setMaximumWidth(250)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.container = QFrame()
        self.container.setFrameShape(QFrame.Shape.StyledPanel)
        self.container.setFrameShadow(QFrame.Shadow.Plain)
        self.container.setLineWidth(2)
        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(5, 5, 10, 10)
        self.container.setLayout(self.container_layout)

        self.layout.addWidget(self.container)

        self.primary_section = QWidget()
        self.primary_layout = QVBoxLayout()
        self.primary_layout.setContentsMargins(0, 0, 0, 0)
        self.primary_section.setLayout(self.primary_layout)

        self.secondary_section = QWidget()
        self.secondary_layout = QVBoxLayout()
        self.secondary_layout.setContentsMargins(0, 0, 0, 0)
        self.secondary_section.setLayout(self.secondary_layout)

        self.container_layout.addWidget(self.primary_section)
        self.add_separator()
        self.container_layout.addWidget(self.secondary_section)
        self.container_layout.addStretch()

    def set_primary_widgets(self, widgets):
        self._clear_layout(self.primary_layout)
        for widget in widgets:
            self.primary_layout.addWidget(widget)

    def set_secondary_widgets(self, widgets):
        self._clear_layout(self.secondary_layout)
        for widget in widgets:
            self.secondary_layout.addWidget(widget)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        separator.setContentsMargins(10, 5, 10, 5)
        self.container_layout.addWidget(separator)