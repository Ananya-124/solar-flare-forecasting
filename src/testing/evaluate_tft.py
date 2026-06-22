import pandas as pd
import numpy as np

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# Load dataset

df = pd.read_csv(
    "data/final/tft_dataset.csv"
)

# last 20%

split = int(len(df) * 0.8)

test = df.iloc[split:].copy()

# Simulated prediction file
# replace later with TFT outputs

y_true = test["target"].values

# baseline threshold
y_pred = (
    test["soft_counts"]
    >
    test["soft_counts"].quantile(0.98)
).astype(int)

print(
    classification_report(
        y_true,
        y_pred
    )
)

print(
    confusion_matrix(
        y_true,
        y_pred
    )
)

print(
    "Accuracy:",
    accuracy_score(
        y_true,
        y_pred
    )
)