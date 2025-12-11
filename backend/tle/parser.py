import pandas as pd
import numpy as np
from sgp4.api import Satrec, days2mdhms
from datetime import datetime


def parse_tle_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    tle_data = []
    norad_id = None

    for i in range(0, len(lines), 2):
        if i + 1 >= len(lines):
            break

        line1 = lines[i][:69]
        line2 = lines[i + 1][:69]

        if norad_id is None:
            norad_id_raw = line1[2:7].strip()
            norad_id = str(int(norad_id_raw))

        rso = Satrec.twoline2rv(line1, line2)

        month, day, hour, minute, second = days2mdhms(rso.epochyr, rso.epochdays)
        micsec = (second - int(second)) * 1e6
        epoch = datetime(int(2000 + rso.epochyr), int(month), int(day),
                         int(hour), int(minute), int(second), int(micsec))

        tle_data.append({
            'time': epoch,
            'a': rso.a * rso.radiusearthkm,
            'e': rso.ecco,
            'i': np.degrees(rso.inclo),
            'raan': np.degrees(rso.nodeo),
            'aop': np.degrees(rso.argpo),
            'ma': np.degrees(rso.mo),
            'bstar': rso.bstar,
            'mean_motion': rso.no_kozai * 60 * 24 / (2 * np.pi),
            'mean_motion_derivative': rso.ndot * 60 * 60 * 24 * 24 / (2 * np.pi),
            'revolution_number': rso.revnum
        })

    df = pd.DataFrame(tle_data)
    df = df.drop_duplicates().reset_index(drop=True)

    return {
        'norad_id': norad_id,
        'dataframe': df
    }