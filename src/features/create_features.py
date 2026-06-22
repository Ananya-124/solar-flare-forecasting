import pandas as pd
import numpy as np
import os

df = pd.read_csv("data/processed/merged.csv")

df["datetime"] = pd.to_datetime(
    df["datetime"],
    utc=True
)

print("Original:", df.shape)

# Set datetime as index BEFORE resampling
df = df.set_index("datetime")

df = (
    df.resample("1min")
      .mean()
)

df = df.reset_index()

print("Resampled:", df.shape)

# Features
df["soft_ma5"] = df["soft_counts"].rolling(5).mean()
df["soft_ma30"] = df["soft_counts"].rolling(30).mean()

df["hard_ma5"] = df["hard_counts"].rolling(5).mean()
df["hard_ma30"] = df["hard_counts"].rolling(30).mean()

df["soft_diff"] = df["soft_counts"].diff()
df["hard_diff"] = df["hard_counts"].diff()

df["soft_std5"] = df["soft_counts"].rolling(5).std()
df["hard_std5"] = df["hard_counts"].rolling(5).std()

df["ratio"] = df["soft_counts"] / (df["hard_counts"] + 1)

# Temporary flare labels
threshold = (
    df["soft_counts"].mean()
    + 4 * df["soft_counts"].std()
)

print("Threshold:", threshold)

df["flare"] = (
    df["soft_counts"] > threshold
).astype(int)

# Forecast next 30 minutes
future_window = 30

target = np.zeros(len(df))

flare = df["flare"].values

for i in range(len(df) - future_window):
    target[i] = flare[
        i+1:i+future_window+1
    ].max()

df["target"] = target.astype(int)

df = df.dropna()

os.makedirs(
    "data/final",
    exist_ok=True
)

df.to_csv(
    "data/final/tft_dataset.csv",
    index=False
)

print("\nDataset Shape:")
print(df.shape)

print("\nFlare Counts:")
print(df["flare"].value_counts())

print("\nTarget Counts:")
print(df["target"].value_counts())