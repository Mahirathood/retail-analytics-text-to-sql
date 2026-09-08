import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

for file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(file)

    print("\n" + "=" * 60)
    print(f"FILE: {file.name}")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst 3 rows:")
    print(df.head(3))