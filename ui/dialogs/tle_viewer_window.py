from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLabel
import os
from datetime import datetime, timedelta


class TLEViewerWindow(QDialog):
    def __init__(self, data_dir, norad_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"TLE Viewer - NORAD ID: {norad_id}")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        self.count_label = QLabel("Loading...")
        layout.addWidget(self.count_label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.load_tles(data_dir, norad_id)

    def parse_tle_epoch(self, line1):
        try:
            epoch_year = int(line1[18:20])
            epoch_day = float(line1[20:32])
            year = 2000 + epoch_year if epoch_year < 57 else 1900 + epoch_year
            base_date = datetime(year, 1, 1)
            return base_date + timedelta(days=epoch_day - 1)
        except:
            return None

    def load_tles(self, data_dir, norad_id):
        tle_file = os.path.join(data_dir, 'objects/txt', f"{norad_id}.txt")

        if not os.path.exists(tle_file):
            self.text_edit.setPlainText(f"No TLE file found for NORAD ID: {norad_id}")
            self.count_label.setText("TLEs: 0")
            return

        try:
            with open(tle_file, 'r') as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]

            tles = []
            for i in range(len(lines) - 1):
                line1, line2 = lines[i], lines[i + 1]
                if line1.startswith('1 ') and line2.startswith('2 '):
                    epoch = self.parse_tle_epoch(line1)
                    tles.append((epoch, line1, line2))

            tles.sort(key=lambda x: x[0] or datetime.min, reverse=True)

            tle_text = []
            for epoch, line1, line2 in tles:
                tle_text.extend([line1, line2, ""])

            self.text_edit.setPlainText("\n".join(tle_text))
            self.count_label.setText(f"TLEs: {len(tles)}")

        except Exception as e:
            self.text_edit.setPlainText(f"Error reading TLE file: {str(e)}")
            self.count_label.setText("TLEs: 0")