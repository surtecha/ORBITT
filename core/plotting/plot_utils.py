import pandas as pd
from datetime import timedelta

def load_filtered_tle(norad_id: str, unit: str, window: int, data_dir="data"):
    try:
        df = pd.read_csv(f"{data_dir}/{norad_id}.csv")
        df["EPOCH"] = pd.to_datetime(df["EPOCH"])

        latest_epoch = df["EPOCH"].max()

        delta = {"D": timedelta(days=window),
                 "W": timedelta(weeks=window),
                 "M": timedelta(days=30 * window)}[unit]

        filtered_df = df[df["EPOCH"] >= latest_epoch - delta]
        return filtered_df
    except Exception as e:
        print(f"Error loading data for {norad_id}: {e}")
        return pd.DataFrame()