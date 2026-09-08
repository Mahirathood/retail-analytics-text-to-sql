import pandas as pd
from pathlib import Path

from src.database import engine


# Location of processed CSV files
DATA_DIR = Path("data/processed")

# Location of raw CSV files
RAW_DATA_DIR = Path("data/raw")


def load_table(file_name, table_name):

    print(f"\nLoading {file_name}...")

    # Read CSV
    df = pd.read_csv(DATA_DIR / file_name)

    print(f"Rows found: {len(df):,}")

    # Load into PostgreSQL
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Table '{table_name}' loaded successfully!")


def load_raw_table(file_name, table_name):

    print(f"\nLoading {file_name}...")

    # Read CSV from raw data folder
    df = pd.read_csv(RAW_DATA_DIR / file_name)

    print(f"Rows found: {len(df):,}")

    # Load into PostgreSQL
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Table '{table_name}' loaded successfully!")


if __name__ == "__main__":

    load_table(
        "orders.csv",
        "orders"
    )

    load_table(
        "customers.csv",
        "customers"
    )

    load_table(
        "order_items.csv",
        "order_items"
    )

    load_table(
        "products.csv",
        "products"
    )

    load_table(
        "payments.csv",
        "payments"
    )

    # Load reviews from raw dataset
    load_raw_table(
        "olist_order_reviews_dataset.csv",
        "order_reviews"
    )

    print("\nAll data loaded successfully!")