from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout
from ui.components.input_folder_selector import InputFolderSelector
from ui.components.progress_bar import ProgressBar
from ui.components.log_viewer import LogViewer


def get_sidebar_widgets():
    primary = [
        QLabel("Input Path"),
        InputFolderSelector(""),
        QPushButton("Run")
    ]

    secondary = [
        QLabel("Number of unique objects: "),
        QLabel("Number of TLEs processed: ")
    ]

    return primary, secondary


def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout()

    layout.addWidget(QLabel("Object Sorting"))
    layout.addWidget(ProgressBar())

    layout.addWidget(QLabel("Converting to CSV"))
    layout.addWidget(ProgressBar())

    log_viewer = LogViewer()
    layout.addWidget(log_viewer, 1)

    widget.setLayout(layout)
    return widget