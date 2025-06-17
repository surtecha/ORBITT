import csv
import os
from datetime import datetime, timedelta

GM = 398600441800000.0
GM13 = GM ** (1.0 / 3.0)
EARTH_RADIUS = 6378.137
PI = 3.14159265358979
TPI86 = 2.0 * PI / 86400.0


def calculate_semi_major_axis(mean_motion):
    return GM13 / ((TPI86 * mean_motion) ** (2.0 / 3.0)) / 1000.0


def calculate_apogee_altitude(mean_motion, eccentricity):
    sma = calculate_semi_major_axis(mean_motion)
    return sma * (1.0 + eccentricity) - EARTH_RADIUS


def calculate_perigee_altitude(mean_motion, eccentricity):
    sma = calculate_semi_major_axis(mean_motion)
    return sma * (1.0 - eccentricity) - EARTH_RADIUS


def extract_mean_motion(line2):
    return float(line2[52:63])


def extract_mean_motion_deriv(line1):
    return float(line1[33:43])


def extract_eccentricity(line2):
    return float('0.' + line2[26:33])


def extract_inclination(line2):
    return float(line2[8:16])


def extract_bstar(line1):
    bstar_str = line1[53:61]
    exp_str = line1[59:61]
    mantissa = float(bstar_str[:6])
    exponent = int(exp_str)
    return mantissa * (10 ** exponent)


def extract_raan(line2):
    return float(line2[17:25])


def extract_arg_perigee(line2):
    return float(line2[34:42])


def extract_epoch_utc(line1):
    try:
        epoch_year = int(line1[18:20])
        epoch_day = float(line1[20:32])

        if epoch_year < 57:
            year = 2000 + epoch_year
        else:
            year = 1900 + epoch_year

        base_date = datetime(year, 1, 1)
        date = base_date + timedelta(days=epoch_day - 1)

        return date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return None


def calculate_all_parameters(line1, line2):
    mean_motion = extract_mean_motion(line2)
    eccentricity = extract_eccentricity(line2)

    return {
        'epoch_utc': extract_epoch_utc(line1),
        'apogee_altitude': calculate_apogee_altitude(mean_motion, eccentricity),
        'perigee_altitude': calculate_perigee_altitude(mean_motion, eccentricity),
        'mean_motion': mean_motion,
        'mean_motion_deriv': extract_mean_motion_deriv(line1),
        'eccentricity': eccentricity,
        'inclination': extract_inclination(line2),
        'bstar': extract_bstar(line1),
        'semi_major_axis': calculate_semi_major_axis(mean_motion),
        'raan': extract_raan(line2),
        'arg_perigee': extract_arg_perigee(line2),
    }


def save_to_csv(data_list, csv_filepath, sort_by='epoch_utc'):
    fieldnames = ['epoch_utc', 'apogee_altitude', 'perigee_altitude', 'mean_motion', 'mean_motion_deriv',
                  'eccentricity', 'inclination', 'bstar', 'semi_major_axis', 'raan', 'arg_perigee']

    sorted_data = sorted(data_list, key=lambda x: x.get(sort_by, ''))

    with open(csv_filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)


def append_to_csv(data_list, csv_filepath, sort_by='epoch_utc'):
    fieldnames = ['epoch_utc', 'apogee_altitude', 'perigee_altitude', 'mean_motion', 'mean_motion_deriv',
                  'eccentricity', 'inclination', 'bstar', 'semi_major_axis', 'raan', 'arg_perigee']

    existing_data = []
    if os.path.exists(csv_filepath):
        with open(csv_filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_data = list(reader)
            for row in existing_data:
                for key in row:
                    if row[key] and key != 'epoch_utc':
                        row[key] = float(row[key])

    existing_epochs = {row['epoch_utc'] for row in existing_data}

    new_data = [row for row in data_list if row['epoch_utc'] not in existing_epochs]

    if new_data:
        combined_data = existing_data + new_data
        sorted_data = sorted(combined_data, key=lambda x: x.get(sort_by, ''))

        with open(csv_filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_data)