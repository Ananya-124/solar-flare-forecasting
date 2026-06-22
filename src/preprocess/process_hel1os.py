from astropy.io import fits
from astropy.time import Time
import pandas as pd
import numpy as np
import os
from glob import glob

BASE_DIR = "data/raw/hel1os"

all_days = []

folders = sorted(
    glob(os.path.join(BASE_DIR, "HLS_*"))
)

print(f"Found {len(folders)} HEL1OS folders")

for folder in folders:

    lc_file = os.path.join(
        folder,
        "cdte",
        "lightcurve_cdte1.fits"
    )

    if not os.path.exists(lc_file):
        print(f"Skipping: {folder}")
        continue

    print(f"Processing: {lc_file}")

    try:

        with fits.open(lc_file) as hdul:

            # HDU 1 contains lightcurve data
            data = hdul[1].data

            # Convert MJD -> datetime
            times = Time(
                np.asarray(data["MJD"], dtype=np.float64),
                format="mjd"
            )

            df = pd.DataFrame({
                "datetime": pd.to_datetime(
                    times.to_datetime()
                ),
                "hard_counts": np.asarray(
                    data["CTR"],
                    dtype=np.float64
                )
            })

            all_days.append(df)

    except Exception as e:
        print(f"Error processing {lc_file}")
        print(e)

if len(all_days) == 0:
    raise ValueError(
        "No HEL1OS lightcurves were loaded."
    )

final_df = pd.concat(
    all_days,
    ignore_index=True
)

final_df = (
    final_df
    .sort_values("datetime")
    .reset_index(drop=True)
)

os.makedirs(
    "data/processed",
    exist_ok=True
)

final_df.to_csv(
    "data/processed/hel1os.csv",
    index=False
)

print("\nSaved HEL1OS data")
print("Final Shape:", final_df.shape)

print("\nHead:")
print(final_df.head())

print("\nDate Range:")
print(final_df["datetime"].min())
print(final_df["datetime"].max())