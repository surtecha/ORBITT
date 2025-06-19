from pathlib import Path
from PySide6.QtCore import QThread, Signal
from core.tle.tle_processor import read_tle_file, read_existing_tles
from core.tle.csv_convertor import calculate_all_parameters, save_to_csv, append_to_csv


class BulkExtractorWorker(QThread):
    log_message = Signal(str)
    metrics_updated = Signal(int, int)
    extraction_progress = Signal(int)
    conversion_progress = Signal(int)
    finished = Signal()

    def __init__(self, input_files, input_folder, objects_folder):
        super().__init__()
        self.input_files = input_files
        self.input_folder = Path(input_folder)
        self.objects_folder = Path(objects_folder)
        self.txt_folder = self.objects_folder / "txt"
        self.csv_folder = self.objects_folder / "csv"
        self.total_tles_processed = 0
        self.unique_norads = set()

    def run(self):
        try:
            self._setup_directories()
            self._process_files()
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

        for file_index, filename in enumerate(self.input_files):
            self._process_single_file(filename, file_index, total_files)

    def _process_single_file(self, filename, file_index, total_files):
        self.log_message.emit(f"📂 Processing file: {filename}")

        input_filepath = self.input_folder / filename
        tle_data = read_tle_file(str(input_filepath))

        if not tle_data:
            self.log_message.emit(f"⚠️ No TLE data found in {filename}")
            self._update_progress_for_skipped_file(file_index, total_files)
            return

        file_tles_count = sum(len(tles) for tles in tle_data.values())
        self.total_tles_processed += file_tles_count

        processed_norads = self._extract_tles_to_files(tle_data, filename)
        self.unique_norads.update(processed_norads)

        self._update_extraction_progress(file_index, total_files)
        self._convert_tles_to_csv(processed_norads, filename, file_index, total_files)

        self.metrics_updated.emit(self.total_tles_processed, len(self.unique_norads))
        self.log_message.emit(f"✅ Completed processing {filename}")

    def _update_progress_for_skipped_file(self, file_index, total_files):
        progress = int(((file_index + 1) / total_files) * 100)
        self.extraction_progress.emit(progress)
        self.conversion_progress.emit(progress)

    def _update_extraction_progress(self, file_index, total_files):
        progress = int(((file_index + 1) / total_files) * 100)
        self.extraction_progress.emit(progress)

    def _extract_tles_to_files(self, tle_data, source_filename):
        processed_norads = set()

        for norad_id, new_tles in tle_data.items():
            output_file = self.txt_folder / f"{norad_id}.txt"

            existing_tles = read_existing_tles(str(output_file)) if output_file.exists() else []
            all_tles = existing_tles + new_tles
            sorted_tles = sorted(all_tles, key=lambda x: x[0] if x[0] else 0)

            with open(output_file, 'w') as file:
                for _, line1, line2 in sorted_tles:
                    file.write(f"{line1}\n{line2}\n")

            processed_norads.add(norad_id)

        self.log_message.emit(f"🔄 Extracted {len(processed_norads)} NORAD objects from {source_filename}")
        return processed_norads

    def _convert_tles_to_csv(self, norad_ids, source_filename, current_file, total_files):
        converted_count = 0
        total_norads = len(norad_ids)

        for i, norad_id in enumerate(norad_ids):
            if self._convert_single_norad_to_csv(norad_id):
                converted_count += 1

            if total_norads > 0:
                file_progress = (i + 1) / total_norads
                overall_progress = ((current_file + file_progress) / total_files) * 100
                self.conversion_progress.emit(int(overall_progress))

        self.log_message.emit(f"📊 Converted {converted_count}/{total_norads} files to CSV from {source_filename}")

    def _convert_single_norad_to_csv(self, norad_id):
        txt_file = self.txt_folder / f"{norad_id}.txt"
        csv_file = self.csv_folder / f"{norad_id}.csv"

        if not txt_file.exists():
            self.log_message.emit(f"  └─ {norad_id}: TXT file not found ❌")
            return False

        try:
            tle_data = read_tle_file(str(txt_file))
            if not tle_data or norad_id not in tle_data:
                self.log_message.emit(f"  └─ {norad_id}: No TLE data found ❌")
                return False

            csv_data = []
            for _, line1, line2 in tle_data[norad_id]:
                try:
                    params = calculate_all_parameters(line1, line2)
                    csv_data.append(params)
                except Exception as e:
                    self.log_message.emit(f"  └─ {norad_id}: Error processing TLE - {str(e)} ❌")
                    continue

            if csv_data:
                if csv_file.exists():
                    append_to_csv(csv_data, str(csv_file))
                else:
                    save_to_csv(csv_data, str(csv_file))
                self.log_message.emit(f"  └─ {norad_id}: Converted to CSV ✅")
                return True
            else:
                self.log_message.emit(f"  └─ {norad_id}: No valid TLE data ❌")
                return False

        except Exception as e:
            self.log_message.emit(f"  └─ {norad_id}: Processing failed - {str(e)} ❌")
            return False

    def _finalize_processing(self):
        self.extraction_progress.emit(100)
        self.conversion_progress.emit(100)
        self.log_message.emit("🎉 All files processed successfully")