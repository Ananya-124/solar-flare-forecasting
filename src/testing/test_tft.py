import pandas as pd
import numpy as np

from pytorch_forecasting import (
    TimeSeriesDataSet,
    TemporalFusionTransformer
)

# -----------------------
# Load dataset
# -----------------------

df = pd.read_csv(
    "data/final/tft_dataset.csv"
)

df["datetime"] = pd.to_datetime(df["datetime"])

df["time_idx"] = np.arange(len(df))
df["series"] = "solar"

# -----------------------
# Split
# -----------------------

train_boundary = int(
    len(df) * 0.8
)

test_df = df.iloc[train_boundary:].copy()

print("Test Shape:", test_df.shape)

# -----------------------
# Recreate dataset
# -----------------------

training = TimeSeriesDataSet(
    df.iloc[:train_boundary],

    time_idx="time_idx",
    target="target",

    group_ids=["series"],

    max_encoder_length=60,
    max_prediction_length=30,

    time_varying_known_reals=[
        "time_idx"
    ],

    time_varying_unknown_reals=[
        "soft_counts",
        "hard_counts",
        "soft_ma5",
        "soft_ma30",
        "hard_ma5",
        "hard_ma30",
        "soft_diff",
        "hard_diff",
        "soft_std5",
        "hard_std5",
        "ratio",
        "target"
    ]
)

test_dataset = TimeSeriesDataSet.from_dataset(
    training,
    test_df,
    predict=True,
    stop_randomization=True
)

test_loader = test_dataset.to_dataloader(
    train=False,
    batch_size=64
)

# -----------------------
# Load model
# -----------------------

tft = TemporalFusionTransformer.load_from_checkpoint(
    "models/tft.ckpt"
)

# -----------------------
# Predict
# -----------------------

predictions = tft.predict(
    test_loader
)

print("Prediction Shape:")
print(predictions.shape)

print("\nFirst Predictions:")
print(predictions[:20])