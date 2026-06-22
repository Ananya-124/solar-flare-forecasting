from astropy.io import fits
import pandas as pd
import numpy as np

lc_path = r"C:\Users\Ananya\OneDrive\Desktop\solar\data\raw\solexs\AL1_SLX_L1_20240710_v1.1\SDD2\AL1_SOLEXS_20240710_SDD2_L1.lc.gz"

with fits.open(lc_path) as hdul:
    data = hdul["RATE"].data

# Convert FITS columns to native numpy arrays
time_sec = np.asarray(data["TIME"], dtype=np.float64)
counts = np.asarray(data["COUNTS"], dtype=np.float64)

df = pd.DataFrame({
    "time_sec": time_sec,
    "counts": counts
})

gti_path = r"C:\Users\Ananya\OneDrive\Desktop\solar\data\raw\solexs\AL1_SLX_L1_20240710_v1.1\SDD2\AL1_SOLEXS_20240710_SDD2_L1.gti.gz"

with fits.open(gti_path) as hdul:
    gti = hdul[1].data

# Convert GTI columns too
starts = np.asarray(gti["START"], dtype=np.float64)
stops = np.asarray(gti["STOP"], dtype=np.float64)

mask = np.zeros(len(df), dtype=bool)

for start, stop in zip(starts, stops):
    mask |= (
        (df["time_sec"].values >= start)
        & (df["time_sec"].values <= stop)
    )

df = df.loc[mask].copy()

print("Rows after GTI:", len(df))
print(df.head())
import pandas as pd

print(pd.to_datetime(1720570000, unit='s', utc=True))