import os
import zipfile
import tempfile
from pathlib import Path

class FileHandler:
    @staticmethod
    def extract_zip_files(zip_files, temp_dir=None):
        if temp_dir is None:
            temp_dir = tempfile.mkdtemp()
        
        extracted_files = []
        
        for zip_file in zip_files:
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    
                    for file_info in zip_ref.filelist:
                        if file_info.filename.endswith('.txt'):
                            extracted_path = os.path.join(temp_dir, file_info.filename)
                            if os.path.exists(extracted_path):
                                extracted_files.append(extracted_path)
                                
            except Exception as e:
                raise Exception(f"Error extracting {zip_file}: {e}")
        
        return extracted_files, temp_dir
    
    @staticmethod
    def validate_tle_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
            
            tle_count = 0
            for i in range(len(lines) - 1):
                if lines[i].strip().startswith('1 ') and lines[i+1].strip().startswith('2 '):
                    tle_count += 1
            
            return tle_count > 0, tle_count
            
        except Exception:
            return False, 0
    
    @staticmethod
    def get_file_size_mb(filepath):
        try:
            size_bytes = os.path.getsize(filepath)
            return size_bytes / (1024 * 1024)
        except Exception:
            return 0
    
    @staticmethod
    def create_directory(path):
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False