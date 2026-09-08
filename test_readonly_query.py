from src.query_validator import run_query

print("Testing run_query with read-only database...")

try:
    result = run_query("""
        SELECT
            order_status,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY order_status
        ORDER BY order_count DESC
    """)

    print("\nQUERY SUCCESSFUL!")
    print(result)

except Exception as e:
    print("\nQUERY FAILED!")
    print("Reason:", e)