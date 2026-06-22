import pandas as pd

soft = pd.read_csv(
    "data/processed/solexs.csv"
)

hard = pd.read_csv(
    "data/processed/hel1os.csv"
)

soft["datetime"] = pd.to_datetime(
    soft["datetime"],
    utc=True
)

hard["datetime"] = pd.to_datetime(
    hard["datetime"],
    utc=True
)

soft = soft.sort_values("datetime")
hard = hard.sort_values("datetime")

print("SoLEXS:", soft.shape)
print("HEL1OS:", hard.shape)

df = pd.merge_asof(
    soft,
    hard,
    on="datetime",
    direction="nearest",
    tolerance=pd.Timedelta("2s")
)

print("Merged:", df.shape)

print(
    "Missing hard counts:",
    df["hard_counts"].isna().sum()
)

df = df.dropna()

print(
    "After dropna:",
    df.shape
)

df.to_csv(
    "data/processed/merged.csv",
    index=False
)