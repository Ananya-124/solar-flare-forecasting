from astropy.io import fits
import pandas as pd
import numpy as np
import os
from glob import glob

BASE_DIR = "data/raw/solexs"

all_days = []

folders = sorted(glob(os.path.join(BASE_DIR, "AL1_SLX_L1_*")))

for folder in folders:

    sdd2 = os.path.join(folder, "SDD2")

    lc_files = glob(os.path.join(sdd2, "*.lc.gz"))

    if len(lc_files) == 0:
        continue

    lc_path = lc_files[0]

    print("Processing:", lc_path)

    with fits.open(lc_path) as hdul:
        data = hdul["RATE"].data

    df = pd.DataFrame({
        "datetime": pd.to_datetime(
            np.asarray(data["TIME"], dtype=np.float64),
            unit="s",
            utc=True
        ),
        "soft_counts": np.asarray(
            data["COUNTS"],
            dtype=np.float64
        )
    })

    all_days.append(df)

final_df = pd.concat(all_days)

final_df = (
    final_df
    .sort_values("datetime")
    .reset_index(drop=True)
)

os.makedirs("data/processed", exist_ok=True)

# Save as CSV (avoid pyarrow issues)
final_df.to_csv(
    "data/processed/solexs.csv",
    index=False
)

print("Final Shape:", final_df.shape)
print(final_df.head())