import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

READONLY_DATABASE_URL = os.getenv("READONLY_DATABASE_URL")

if not READONLY_DATABASE_URL:
    raise ValueError("READONLY_DATABASE_URL not found in .env")

readonly_engine = create_engine(READONLY_DATABASE_URL)

print("Testing read-only database connection...")

with readonly_engine.connect() as connection:

    # Check which PostgreSQL user is actually connected
    result = connection.execute(
        text("""
            SELECT current_user, session_user, current_database();
        """)
    )

    user_info = result.fetchone()

    print("\nCONNECTION INFORMATION")
    print("----------------------")
    print("Current user:", user_info[0])
    print("Session user:", user_info[1])
    print("Database:", user_info[2])

    # Test SELECT
    result = connection.execute(
        text("SELECT COUNT(*) FROM orders")
    )

    print("\nSELECT test:", result.scalar())

    # Test UPDATE
    print("\nTesting UPDATE protection...")

    try:
        connection.execute(
            text("""
                UPDATE orders
                SET order_status = order_status
                WHERE false
            """)
        )

        print("ERROR: UPDATE was allowed!")

    except Exception as e:
        print("UPDATE correctly blocked!")
        print("Reason:", e)