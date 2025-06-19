import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import os

def filter_data_by_timeframe(df, timeframe, days_back):
    df['epoch_utc'] = pd.to_datetime(df['epoch_utc'])
    end_date = df['epoch_utc'].max()

    multiplier = {'D': 1, 'W': 7, 'M': 30}.get(timeframe, 1)
    start_date = end_date - timedelta(days=days_back * multiplier)

    return df[(df['epoch_utc'] >= start_date) & (df['epoch_utc'] <= end_date)]


def load_satellite_data(data_dir, norad_id):
    csv_subdir = os.path.join(data_dir, 'objects/csv')
    csv_path = os.path.join(csv_subdir, f"{norad_id}.csv")

    if not os.path.exists(csv_path):
        return None

    try:
        df = pd.read_csv(csv_path)
        df['epoch_utc'] = pd.to_datetime(df['epoch_utc'])
        return df.sort_values('epoch_utc')
    except Exception:
        return None


def create_preview_plot(df, y_column, title, ylabel):
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    valid_data = df.dropna(subset=['epoch_utc', y_column])
    if len(valid_data) == 0:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return fig

    x_data, y_data = valid_data['epoch_utc'], valid_data[y_column].astype(float)

    ax.plot(x_data, y_data, color='#2563eb', linewidth=2, alpha=0.9)

    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')

    for spine in ax.spines.values():
        spine.set_visible(False)

    y_range = y_data.max() - y_data.min()
    if y_range > 0:
        margin = y_range * 0.05
        ax.set_ylim(y_data.min() - margin, y_data.max() + margin)

    plt.tight_layout()
    return fig


def get_plot_sections():
    return {
        "Altitude": {
            "plots": [
                {"column": "perigee_altitude", "title": "Perigee Altitude", "ylabel": "Altitude (km)"},
                {"column": "apogee_altitude", "title": "Apogee Altitude", "ylabel": "Altitude (km)"}
            ]
        },
        "Shape & Size": {
            "plots": [
                {"column": "semi_major_axis", "title": "Semi-Major Axis", "ylabel": "SMA (km)"},
                {"column": "eccentricity", "title": "Eccentricity", "ylabel": "Eccentricity"}
            ]
        },
        "Drag": {
            "plots": [
                {"column": "bstar", "title": "B* Drag Term", "ylabel": "B* (1/earth radii)"}
            ]
        },
        "Mean Motion": {
            "plots": [
                {"column": "mean_motion", "title": "Mean Motion", "ylabel": "Rev/day"},
                {"column": "mean_motion_deriv", "title": "Mean Motion Derivative", "ylabel": "Rev/day²"}
            ]
        },
        "Angular Elements": {
            "plots": [
                {"column": "inclination", "title": "Inclination", "ylabel": "Degrees"},
                {"column": "raan", "title": "RAAN", "ylabel": "Degrees"},
                {"column": "arg_perigee", "title": "Argument of Perigee", "ylabel": "Degrees"}
            ]
        }
    }