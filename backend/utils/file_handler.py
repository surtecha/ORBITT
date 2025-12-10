from PySide6.QtWidgets import QFileDialog

_last_directory = ""
_last_filter = "Text Files (*.txt)"

def open_tle_file():
    global _last_directory, _last_filter
    
    filters = "Text Files (*.txt);;TLE Files (*.tle);;All Files (*.*)"
    
    filepath, selected_filter = QFileDialog.getOpenFileName(
        None,
        "Select TLE File",
        _last_directory,
        filters,
        _last_filter
    )
    
    if filepath:
        import os
        _last_directory = os.path.dirname(filepath)
        _last_filter = selected_filter
        return filepath
    
    return None