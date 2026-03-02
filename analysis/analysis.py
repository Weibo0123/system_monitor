#analysis.py
import pandas as pd
import os

INPUT_CSV = "logs/system_log.csv"
OUT_DIR = "analysis_output"
CLEANED_CSV = os.path.join(OUT_DIR, "cleaned_log.csv")
SUMMARY_CSV = os.path.join(OUT_DIR, "summary.csv")

REQUIRED_COLS = ["timestamp", "cpu", "mem", "disk", "net_up", "net_down"]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [i for i in REQUIRED_COLS if i not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df




def main():
    df = pd.read_csv('logs/system_log.csv')

    print(df.head())
    df.info()
    print(df.describe())

if __name__ == '__main__':
    main()