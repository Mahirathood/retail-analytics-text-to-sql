from src.query_validator import validate_sql, enforce_limit


tests = [
    (
        "Safe SELECT",
        "SELECT * FROM orders"
    ),
    (
        "Safe SELECT with LIMIT",
        "SELECT * FROM orders LIMIT 10"
    ),
    (
        "LIMIT too large",
        "SELECT * FROM orders LIMIT 50000"
    ),
    (
        "Dangerous INSERT",
        "INSERT INTO orders VALUES ('test')"
    ),
    (
        "Dangerous DELETE",
        "DELETE FROM orders"
    ),
    (
        "Dangerous DROP",
        "DROP TABLE orders"
    ),
    (
        "Dangerous UPDATE",
        "UPDATE orders SET order_status = 'delivered'"
    ),
    (
        "Dangerous ALTER",
        "ALTER TABLE orders ADD COLUMN test TEXT"
    ),
    (
        "Multiple statements",
        "SELECT * FROM orders; DROP TABLE customers"
    ),
    (
        "Non-SQL command",
        "DROP DATABASE retail_analytics"
    ),
]


for name, sql in tests:

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    try:

        validated = validate_sql(sql)
        safe_sql = enforce_limit(validated)

        print("STATUS: ALLOWED")
        print("SQL:")
        print(safe_sql)

    except Exception as e:

        print("STATUS: BLOCKED")
        print("Reason:", e)