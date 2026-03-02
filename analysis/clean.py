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

