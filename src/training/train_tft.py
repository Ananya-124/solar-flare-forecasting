import pandas as pd
import numpy as np

from pytorch_forecasting import (
    TimeSeriesDataSet,
    TemporalFusionTransformer
)

from pytorch_forecasting.metrics import QuantileLoss

from lightning.pytorch import Trainer

# -----------------
# Load Dataset
# -----------------

df = pd.read_csv(
    "data/final/tft_dataset.csv"
)

df["datetime"] = pd.to_datetime(df["datetime"])

# Create sequential index
df["time_idx"] = np.arange(len(df))

# Single time series
df["series"] = "solar"

# -----------------
# Train/Val Split
# -----------------

train_boundary = int(
    len(df) * 0.8
)

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

validation = TimeSeriesDataSet.from_dataset(
    training,
    df.iloc[train_boundary:],
    predict=True,
    stop_randomization=True
)

train_loader = training.to_dataloader(
    train=True,
    batch_size=64
)

val_loader = validation.to_dataloader(
    train=False,
    batch_size=64
)

# -----------------
# Model
# -----------------

tft = TemporalFusionTransformer.from_dataset(
    training,

    hidden_size=16,

    attention_head_size=4,

    dropout=0.1,

    hidden_continuous_size=8,

    learning_rate=1e-3,

    loss=QuantileLoss()
)

# -----------------
# Training
# -----------------

trainer = Trainer(
    max_epochs=10,
    accelerator="auto"
)

trainer.fit(
    tft,
    train_loader,
    val_loader
)

trainer.save_checkpoint(
    "models/tft.ckpt"
)