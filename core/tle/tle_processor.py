import os
import re
from datetime import datetime, timedelta


def parse_tle_epoch(line1):
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


def extract_norad_id(line1):
    match = re.search(r'^\d\s+(\d+)', line1)
    if match:
        return int(match.group(1))
    return None


def read_tle_file(filepath):
    tle_data = {}

    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]

        i = 0
        while i < len(lines) - 1:
            line1 = lines[i]
            line2 = lines[i + 1]

            if line1.startswith('1 ') and line2.startswith('2 '):
                norad_id = extract_norad_id(line1)
                epoch = parse_tle_epoch(line1)

                if norad_id:
                    if norad_id not in tle_data:
                        tle_data[norad_id] = []
                    tle_data[norad_id].append((epoch, line1, line2))
            i += 1

        return tle_data
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return {}


def read_existing_tles(filepath):
    tle_list = []

    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]

        i = 0
        while i < len(lines) - 1:
            line1 = lines[i]
            line2 = lines[i + 1]

            if line1.startswith('1 ') and line2.startswith('2 '):
                epoch = parse_tle_epoch(line1)
                tle_list.append((epoch, line1, line2))
            i += 1

    except:
        pass

    return tle_list


def process_tle_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_dir, filename)
            tle_data = read_tle_file(filepath)

            for norad_id, new_tles in tle_data.items():
                output_file = os.path.join(output_dir, f"{norad_id}.txt")

                existing_tles = read_existing_tles(output_file)
                all_tles = existing_tles + new_tles
                sorted_tles = sorted(all_tles, key=lambda x: x[0] if x[0] else datetime.min)

                with open(output_file, 'w') as file:
                    for _, line1, line2 in sorted_tles:
                        file.write(f"{line1}\n{line2}\n")