import pandas as pd


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


def check_data_quality(df, name):

    print("\n" + "=" * 60)
    print(f"DATA QUALITY CHECK: {name}")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nData types:")
    print(df.dtypes)


def inspect_order_missing_values(orders):

    print("\n" + "=" * 60)
    print("ORDERS - MISSING VALUE ANALYSIS")
    print("=" * 60)

    missing_columns = [
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date"
    ]

    for column in missing_columns:

        print(f"\n--- {column} ---")

        missing_rows = orders[orders[column].isnull()]

        print(f"Missing rows: {len(missing_rows)}")

        print("\nOrder status:")
        print(
            missing_rows["order_status"].value_counts()
        )

        print("\nSample rows:")
        print(
            missing_rows[
                ["order_id", "order_status", column]
            ].head(10)
        )


def inspect_product_missing_values(products):

    print("\n" + "=" * 60)
    print("PRODUCTS - MISSING VALUE ANALYSIS")
    print("=" * 60)

    missing_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for column in missing_columns:

        print(f"\n--- {column} ---")

        missing_rows = products[products[column].isnull()]

        print(f"Missing rows: {len(missing_rows)}")

        print("\nSample rows:")
        print(
            missing_rows[
                ["product_id", column]
            ].head(10)
        )


if __name__ == "__main__":

    orders, customers, order_items, products, payments = load_data()

    check_data_quality(orders, "Orders")
    check_data_quality(customers, "Customers")
    check_data_quality(order_items, "Order Items")
    check_data_quality(products, "Products")
    check_data_quality(payments, "Payments")

    inspect_order_missing_values(orders)

    inspect_product_missing_values(products)