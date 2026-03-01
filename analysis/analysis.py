import pandas as pd

def main():
    df = pd.read_csv('logs/system_log.csv')

    print(df.head())
    df.info()
    print(df.describe())

if __name__ == '__main__':
    main()