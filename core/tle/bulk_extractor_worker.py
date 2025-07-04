from pathlib import Path
from PySide6.QtCore import QThread, Signal
import csv
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from core.tle.tle_processor import read_tle_file, read_existing_tles, parse_tle_epoch, extract_norad_id
from core.tle.csv_convertor import calculate_all_parameters, save_to_csv, append_to_csv


class BulkExtractorWorker(QThread):
    log_message = Signal(str)
    metrics_updated = Signal(int, int)
    extraction_progress = Signal(int)
    conversion_progress = Signal(int)
    finished = Signal()

    def __init__(self, input_files: List[str], input_folder: str, objects_folder: str):
        super().__init__()
        self.input_files = input_files
        self.input_folder = Path(input_folder)
        self.objects_folder = Path(objects_folder)
        self.txt_folder = self.objects_folder / "txt"
        self.csv_folder = self.objects_folder / "csv"
        self.total_tles_processed = 0
        self.unique_norads: Set[str] = set()

    def run(self):
        try:
            self._setup_directories()
            self._process_files()
            self._convert_to_csv()
            self._finalize_processing()
        except Exception as e:
            self.log_message.emit(f"❌ Error during processing: {str(e)}")
        finally:
            self.finished.emit()

    def _setup_directories(self):
        self.txt_folder.mkdir(parents=True, exist_ok=True)
        self.csv_folder.mkdir(parents=True, exist_ok=True)

    def _process_files(self):
        total_files = len(self.input_files)
        batch_size = max(1, total_files // 20)

        for file_index, filename in enumerate(self.input_files):
            self.log_message.emit(f"📂 Processing file: {filename}")

            input_filepath = self.input_folder / filename
            tle_data = read_tle_file(str(input_filepath))

            if not tle_data:
                self.log_message.emit(f"⚠️ No TLE data found in {filename}")
                self.extraction_progress.emit(int(((file_index + 1) / total_files) * 100))
                continue

            file_tles_count = sum(len(tles) for tles in tle_data.values())
            self.total_tles_processed += file_tles_count

            self._extract_tles_to_files(tle_data, filename)
            self.unique_norads.update(tle_data.keys())

            if file_index % batch_size == 0 or file_index == total_files - 1:
                self.extraction_progress.emit(int(((file_index + 1) / total_files) * 100))
                self.metrics_updated.emit(self.total_tles_processed, len(self.unique_norads))

            self.log_message.emit(f"✅ Completed processing {filename}")

    def _convert_to_csv(self):
        txt_files = list(self.txt_folder.glob("*.txt"))
        total_files = len(txt_files)

        if total_files == 0:
            return

        batch_size = max(1, total_files // 20)

        for file_index, txt_file in enumerate(txt_files):
            norad_id = txt_file.stem
            csv_file = self.csv_folder / f"{norad_id}.csv"

            try:
                latest_epoch = self._get_latest_epoch_from_csv(csv_file)
                tle_data = read_tle_file(str(txt_file))

                if not tle_data or norad_id not in tle_data:
                    continue

                new_tles = []
                for epoch, line1, line2 in tle_data[norad_id]:
                    if epoch and (not latest_epoch or epoch > latest_epoch):
                        new_tles.append((epoch, line1, line2))

                if new_tles:
                    new_tles.sort(key=lambda x: x[0])
                    csv_data = []

                    for _, line1, line2 in new_tles:
                        try:
                            params = calculate_all_parameters(line1, line2)
                            csv_data.append(params)
                        except:
                            continue

                    if csv_data:
                        if csv_file.exists():
                            append_to_csv(csv_data, str(csv_file))
                        else:
                            save_to_csv(csv_data, str(csv_file))
                        self.log_message.emit(f"  └─ {norad_id}: Updated CSV with {len(csv_data)} new records ✅")
                    else:
                        self.log_message.emit(f"  └─ {norad_id}: No valid new data ❌")
                else:
                    self.log_message.emit(f"  └─ {norad_id}: No new epochs found ⏭️")

            except Exception as e:
                self.log_message.emit(f"  └─ {norad_id}: Processing failed - {str(e)} ❌")

            if file_index % batch_size == 0 or file_index == total_files - 1:
                self.conversion_progress.emit(int(((file_index + 1) / total_files) * 100))

    def _extract_tles_to_files(self, tle_data: Dict[str, List[Tuple]], source_filename: str):
        for norad_id, new_tles in tle_data.items():
            output_file = self.txt_folder / f"{norad_id}.txt"

            existing_tles = read_existing_tles(str(output_file)) if output_file.exists() else []
            all_tles = existing_tles + new_tles
            all_tles.sort(key=lambda x: x[0] if x[0] else datetime.min)

            with open(output_file, 'w', encoding='utf-8') as file:
                for _, line1, line2 in all_tles:
                    file.write(f"{line1}\n{line2}\n")

    def _get_latest_epoch_from_csv(self, csv_file: Path) -> Optional[datetime]:
        if not csv_file.exists():
            return None

        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                latest_epoch = None
                for row in reader:
                    if row['epoch_utc']:
                        epoch_dt = datetime.strptime(row['epoch_utc'], '%Y-%m-%d %H:%M:%S')
                        if not latest_epoch or epoch_dt > latest_epoch:
                            latest_epoch = epoch_dt
                return latest_epoch
        except:
            return None

    def _finalize_processing(self):
        self.extraction_progress.emit(100)
        self.conversion_progress.emit(100)
        self.log_message.emit("🎉 All files processed successfully")