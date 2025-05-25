import os
import re
import glob
from datetime import datetime, timedelta

class TLEExtractor:
    def __init__(self):
        pass
        
    def parse_tle_epoch(self, line1):
        try:
            epoch_year = int(line1[18:20])
            epoch_day = float(line1[20:32])
            
            if epoch_year < 57:
                year = 2000 + epoch_year
            else:
                year = 1900 + epoch_year
                
            base_date = datetime(year, 1, 1)
            date = base_date + timedelta(days=epoch_day - 1)
            
            return date
        except:
            return None

    def extract_norad_id(self, line1):
        match = re.search(r'^\d\s+(\d+)', line1)
        if match:
            return int(match.group(1))
        return None

    def read_tle_file(self, filepath):
        tle_data = {}
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
            
            lines = [line.strip() for line in lines]
            
            i = 0
            while i < len(lines) - 1:
                line1 = lines[i]
                line2 = lines[i+1]
                
                if line1.startswith('1 ') and line2.startswith('2 '):
                    norad_id = self.extract_norad_id(line1)
                    
                    if norad_id:
                        epoch = self.parse_tle_epoch(line1)
                        
                        if norad_id not in tle_data:
                            tle_data[norad_id] = []
                        
                        tle_data[norad_id].append((epoch, line1, line2))
                    
                i += 1
            
            return tle_data
        
        except Exception as e:
            raise Exception(f"Error reading file {filepath}: {e}")

    def create_norad_id_file(self, norad_id, tle_list, output_dir):
        filepath = os.path.join(output_dir, f"{norad_id}.txt")
        existing_tles = []
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                    
                lines = [line.strip() for line in lines]
                
                i = 0
                while i < len(lines) - 1:
                    if lines[i].startswith('1 ') and lines[i+1].startswith('2 '):
                        epoch = self.parse_tle_epoch(lines[i])
                        existing_tles.append((epoch, lines[i], lines[i+1]))
                    i += 1
            except Exception:
                existing_tles = []
        
        all_tles = existing_tles + tle_list
        
        unique_tles = {}
        for epoch, line1, line2 in all_tles:
            if epoch is not None:
                key = f"{epoch}_{hash(line1+line2)}"
                if key not in unique_tles:
                    unique_tles[key] = (epoch, line1, line2)
        
        sorted_tles = sorted([v for v in unique_tles.values()], key=lambda x: x[0] if x[0] else datetime.min)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                for _, line1, line2 in sorted_tles:
                    file.write(f"{line1}\n{line2}\n")
        except Exception as e:
            raise Exception(f"Error writing file {filepath}: {e}")
        
        return len(sorted_tles)

    def process_tle_files(self, input_files, output_dir, progress_callback=None):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        total_files_processed = 0
        total_objects_found = 0
        total_tles_processed = 0
        processed_norad_ids = set()
        
        if progress_callback:
            progress_callback(f"Found {len(input_files)} TLE files to process")
        
        for file_path in input_files:
            try:
                filename = os.path.basename(file_path)
                if progress_callback:
                    progress_callback(f"Processing {filename}...")
                
                tle_data = self.read_tle_file(file_path)
                
                for norad_id, tle_list in tle_data.items():
                    tle_count = self.create_norad_id_file(norad_id, tle_list, output_dir)
                    
                    total_tles_processed += len(tle_list)
                    
                    if norad_id not in processed_norad_ids:
                        processed_norad_ids.add(norad_id)
                        total_objects_found += 1
                    
                    if progress_callback:
                        progress_callback(f"  - NORAD ID {norad_id}: {len(tle_list)} TLEs (total: {tle_count})")
                
                total_files_processed += 1
                
            except Exception as e:
                if progress_callback:
                    progress_callback(f"Error processing file {file_path}: {e}")
                continue
        
        results = {
            'files_processed': total_files_processed,
            'objects_found': total_objects_found,
            'tles_processed': total_tles_processed,
            'output_dir': output_dir
        }
        
        if progress_callback:
            progress_callback("Processing complete!")
            progress_callback(f"Files processed: {total_files_processed}")
            progress_callback(f"Unique objects found: {total_objects_found}")
            progress_callback(f"Total TLEs processed: {total_tles_processed}")
            progress_callback(f"Output directory: {output_dir}")
        
        return results