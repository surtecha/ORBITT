import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import re
from PyQt5.QtCore import QThread, pyqtSignal

GM = 398600441800000.0
GM13 = GM ** (1.0/3.0)
MRAD = 6378.137
PI = math.pi
TPI86 = 2.0 * PI / 86400.0

class CSVConverter:
    def __init__(self):
        pass
    
    def tle_epoch_to_datetime(self, tle_epoch_str):
        year_short = int(tle_epoch_str[:2])
        day_of_year_fraction = float(tle_epoch_str[2:])
        
        if year_short < 57:
            year = 2000 + year_short
        else:
            year = 1900 + year_short
        
        start_of_year = datetime(year, 1, 1)
        delta_days = timedelta(days=(day_of_year_fraction - 1))
        epoch_datetime = start_of_year + delta_days
        return epoch_datetime
    
    def parse_scientific_notation(self, field):
        field = field.strip()
        match = re.match(r'([ +-])?(\d+)([+-]\d)', field)
        if match:
            sign_char, mantissa_str, exponent_str = match.groups()
            sign = -1.0 if sign_char == '-' else 1.0
            mantissa = float(f'0.{mantissa_str}')
            exponent = int(exponent_str)
            return sign * mantissa * (10 ** exponent)
        else:
            try:
                if float(field) == 0.0:
                    return 0.0
            except ValueError:
                pass
            return None
    
    def extract_tle_data(self, line1, line2):
        try:
            epoch_str = line1[18:32].strip()
            epoch_dt = self.tle_epoch_to_datetime(epoch_str)
            epoch_utc = epoch_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            norad_id = int(line1[2:7].strip())
            classification = line1[7:8].strip()
            international_designator = line1[9:17].strip()
            first_deriv_str = line1[33:43].strip()
            second_deriv_str = line1[44:52].strip()
            bstar_str = line1[53:61].strip()
            ephemeris_type = int(line1[62:63].strip()) if line1[62:63].strip() else 0
            element_number = int(line1[64:68].strip())
            
            inclination_deg = float(line2[8:16].strip())
            raan_deg = float(line2[17:25].strip())
            eccentricity_str = line2[26:33].strip()
            arg_perigee_deg = float(line2[34:42].strip())
            mean_anomaly_deg = float(line2[43:51].strip())
            mean_motion_rev_day = float(line2[52:63].strip())
            revolution_number = int(line2[63:68].strip())
            
            eccentricity = float(f'0.{eccentricity_str}')
            first_deriv = float(first_deriv_str) * 2.0
            
            second_deriv_parsed = self.parse_scientific_notation(second_deriv_str)
            if second_deriv_parsed is None:
                second_deriv_parsed = 0.0
            
            bstar = self.parse_scientific_notation(bstar_str)
            if bstar is None:
                return None
            
            mmoti = mean_motion_rev_day
            ecc = eccentricity
            
            if mmoti <= 0:
                return None
            
            sma = GM13 / ((TPI86 * mmoti) ** (2.0 / 3.0)) / 1000.0
            apo = sma * (1.0 + ecc) - MRAD
            per = sma * (1.0 - ecc) - MRAD
            
            period_minutes = 1440.0 / mmoti if mmoti > 0 else 0
            
            return {
                'epoch': epoch_dt,
                'epoch_utc': epoch_utc,
                'norad_id': norad_id,
                'classification': classification,
                'international_designator': international_designator,
                'ephemeris_type': ephemeris_type,
                'element_number': element_number,
                'revolution_number': revolution_number,
                'inclination': inclination_deg,
                'raan': raan_deg,
                'eccentricity': eccentricity,
                'arg_perigee': arg_perigee_deg,
                'mean_anomaly': mean_anomaly_deg,
                'mean_motion': mean_motion_rev_day,
                'mean_motion_derivative': first_deriv,
                'mean_motion_second_derivative': second_deriv_parsed,
                'bstar': bstar,
                'semi_major_axis': sma,
                'apogee_altitude': apo,
                'perigee_altitude': per,
                'period': period_minutes
            }
        except Exception:
            return None
    
    def process_file(self, filepath):
        data_list = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            i = 0
            while i < len(lines) - 1:
                line1 = lines[i].strip()
                line2 = lines[i+1].strip()
                
                if line1.startswith('1 ') and line2.startswith('2 '):
                    tle_data = self.extract_tle_data(line1, line2)
                    if tle_data:
                        data_list.append(tle_data)
                    i += 2
                else:
                    i += 1
            
            if data_list:
                df = pd.DataFrame(data_list)
                df = df.sort_values(by='epoch').reset_index(drop=True)
                return df
            else:
                return None
                
        except Exception:
            return None

class CSVConversionWorker(QThread):
    progress_updated = pyqtSignal(int)
    file_progress_updated = pyqtSignal(str)
    conversion_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, input_files, output_dir):
        super().__init__()
        self.input_files = input_files
        self.output_dir = output_dir
        self.converter = CSVConverter()
    
    def run(self):
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            
            total_files = len(self.input_files)
            processed_files = 0
            successful_conversions = 0
            failed_conversions = 0
            total_records = 0
            
            for i, filepath in enumerate(self.input_files):
                filename = os.path.basename(filepath)
                self.file_progress_updated.emit(f"Processing: {filename}")
                
                try:
                    df = self.converter.process_file(filepath)
                    
                    if df is not None and not df.empty:
                        norad_id = os.path.splitext(filename)[0]
                        output_filepath = os.path.join(self.output_dir, f"{norad_id}.csv")
                        df.to_csv(output_filepath, index=False)
                        successful_conversions += 1
                        total_records += len(df)
                        self.file_progress_updated.emit(f"Completed: {filename} ({len(df)} records)")
                    else:
                        failed_conversions += 1
                        self.file_progress_updated.emit(f"Skipped: {filename} (no valid data)")
                
                except Exception as e:
                    failed_conversions += 1
                    self.file_progress_updated.emit(f"Error processing {filename}: {str(e)}")
                
                processed_files += 1
                progress_percentage = int((processed_files / total_files) * 100)
                self.progress_updated.emit(progress_percentage)
            
            results = {
                'total_files': total_files,
                'successful_conversions': successful_conversions,
                'failed_conversions': failed_conversions,
                'total_records': total_records,
                'output_dir': self.output_dir
            }
            
            self.conversion_completed.emit(results)
            
        except Exception as e:
            self.error_occurred.emit(f"Conversion failed: {str(e)}")