from PySide6.QtWidgets import QFileDialog

def open_tle_file():
    filepath, _ = QFileDialog.getOpenFileName(
        None,
        "Select TLE File",
        "",
        "TLE Files (*.tle);;Text Files (*.txt);;All Files (*.*)"
    )
    return filepath if filepath else None