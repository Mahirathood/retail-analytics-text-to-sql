from sqlalchemy import text

from src.database import engine


def get_schema():

    query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name IN (
          'orders',
          'customers',
          'order_items',
          'products',
          'payments'
      )
    ORDER BY table_name, ordinal_position;
    """

    with engine.connect() as connection:

        result = connection.execute(text(query))

        rows = result.fetchall()

    return rows


if __name__ == "__main__":

    print("\nDATABASE SCHEMA\n")

    rows = get_schema()

    current_table = None

    for table_name, column_name, data_type in rows:

        if table_name != current_table:

            print(f"\nTable: {table_name}")
            print("-" * 40)

            current_table = table_name

        print(f"{column_name} : {data_type}")