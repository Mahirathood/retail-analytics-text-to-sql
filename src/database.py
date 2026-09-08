import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Write connection
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL)


# Read-only connection
READONLY_DATABASE_URL = os.getenv("READONLY_DATABASE_URL")

if not READONLY_DATABASE_URL:
    raise ValueError("READONLY_DATABASE_URL not found in .env file")

readonly_engine = create_engine(READONLY_DATABASE_URL)


# Test write/admin connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        print("Database connection successful!")
        print("Test result:", result.fetchone())

except Exception as e:
    print("Database connection failed!")
    print("Error:", e)