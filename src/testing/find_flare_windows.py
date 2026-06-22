import pandas as pd

df = pd.read_csv(
    "data/final/tft_dataset.csv"
)

flare_rows = df[df["target"] == 1]

print(flare_rows.shape)

print(
    flare_rows[
        [
            "datetime",
            "soft_counts",
            "hard_counts"
        ]
    ].head(50)
)