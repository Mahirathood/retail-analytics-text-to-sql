import pandas as pd
from pathlib import Path


def load_data():

    orders = pd.read_csv(
        "data/raw/olist_orders_dataset.csv"
    )

    customers = pd.read_csv(
        "data/raw/olist_customers_dataset.csv"
    )

    order_items = pd.read_csv(
        "data/raw/olist_order_items_dataset.csv"
    )

    products = pd.read_csv(
        "data/raw/olist_products_dataset.csv"
    )

    payments = pd.read_csv(
        "data/raw/olist_order_payments_dataset.csv"
    )

    return orders, customers, order_items, products, payments


def clean_orders(orders):

    orders = orders.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:

        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )

    return orders


def clean_products(products):

    products = products.copy()

    products["product_category_name"] = (
        products["product_category_name"]
        .fillna("unknown")
    )

    return products


def save_processed_data(
    orders,
    customers,
    order_items,
    products,
    payments
):

    output_dir = Path("data/processed")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    orders.to_csv(
        output_dir / "orders.csv",
        index=False
    )

    customers.to_csv(
        output_dir / "customers.csv",
        index=False
    )

    order_items.to_csv(
        output_dir / "order_items.csv",
        index=False
    )

    products.to_csv(
        output_dir / "products.csv",
        index=False
    )

    payments.to_csv(
        output_dir / "payments.csv",
        index=False
    )

    print("\nProcessed data saved successfully!")


if __name__ == "__main__":

    # Load raw data
    orders, customers, order_items, products, payments = load_data()

    # Clean data
    orders = clean_orders(orders)
    products = clean_products(products)

    # Save cleaned data
    save_processed_data(
        orders,
        customers,
        order_items,
        products,
        payments
    )

    # Display results
    print("\nData cleaning completed successfully!")

    print("\nOrders data types:")
    print(orders.dtypes)

    print("\nProducts missing values:")
    print(products.isnull().sum())