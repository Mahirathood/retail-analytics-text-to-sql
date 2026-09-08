from sqlalchemy import text

from src.database import engine


def run_query(query):

    with engine.connect() as connection:

        result = connection.execute(text(query))

        rows = result.fetchall()

        for row in rows:
            print(row)


if __name__ == "__main__":

    print("\n--- Orders ---")
    run_query("""
        SELECT COUNT(*)
        FROM orders;
    """)

    print("\n--- Customers ---")
    run_query("""
        SELECT COUNT(*)
        FROM customers;
    """)

    print("\n--- Order Items ---")
    run_query("""
        SELECT COUNT(*)
        FROM order_items;
    """)

    print("\n--- Products ---")
    run_query("""
        SELECT COUNT(*)
        FROM products;
    """)

    print("\n--- Payments ---")
    run_query("""
        SELECT COUNT(*)
        FROM payments;
    """)