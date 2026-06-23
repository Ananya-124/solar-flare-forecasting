import pandas as pd

df = pd.read_csv("data/final/tft_dataset.csv")

print(df.columns.tolist())
print(df.head())