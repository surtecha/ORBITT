from PySide6.QtWidgets import QFileDialog, QMessageBox
import os

_last_directory = ""

def open_tle_file():
    global _last_directory
    
    filters = "TLE Files (*.tle *.txt);;All Files (*.*)"
    
    filepath, _ = QFileDialog.getOpenFileName(
        None,
        "Select TLE File",
        _last_directory,
        filters
    )
    
    if filepath:
        if not _validate_tle_file(filepath):
            QMessageBox.critical(
                None,
                "Invalid TLE File",
                f"The selected file does not appear to be a valid TLE file.\n\n"
                f"File: {os.path.basename(filepath)}"
            )
            return None
        
        _last_directory = os.path.dirname(filepath)
        return filepath
    
    return None

def _validate_tle_file(filepath):
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        if len(lines) < 2:
            return False
        
        for i in range(0, len(lines), 2):
            if i + 1 >= len(lines):
                break
            
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip()
            
            if not line1.startswith('1 ') or not line2.startswith('2 '):
                return False
            
            if len(line1) < 69 or len(line2) < 69:
                return False
        
        return True
    except Exception:
        return False