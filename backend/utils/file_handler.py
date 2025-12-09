from PySide6.QtWidgets import QFileDialog

def open_tle_file():
    filepath, _ = QFileDialog.getOpenFileName(
        None,
        "Select TLE File",
        "",
        "Text Files (*.txt);;TLE Files (*.tle);;All Files (*.*)"
    )
    return filepath if filepath else None