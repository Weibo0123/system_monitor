#clean.py
import pandas as pd

NUMERIC_COLS = ["cpu", "mem", "disk", "net_up", "net_down"]

def convert_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df

def convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by=['timestamp'])
    return df.drop_duplicates(subset=['timestamp'], keep="last")

def drop_missing(df: pd.DataFrame, cols=("timestamp", *NUMERIC_COLS)) -> pd.DataFrame:
    return df.dropna(subset=list(cols))

def validate_range(df: pd.DataFrame) -> pd.DataFrame:
    r = (
        df["cpu"].between(0, 100) &
        df["mem"].between(0, 100) &
        df["disk"].between(0, 100)
    )
    return df[range]

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["net_total"] = df["net_up"] + df["net_down"]
    df = df.set_index("timestamp")
    df["cpu_roll_mean_5"] = df["cpu"].rolling(window=5, min_periods=1).mean()
    df["net_roll_mean_5"] = df["net_total"].rolling(window=5, min_periods=1).mean()
    return df

