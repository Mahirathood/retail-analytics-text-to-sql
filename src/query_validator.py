# import re
# import pandas as pd

# from src.database import engine

# def clean_sql(sql):

#     # Remove Markdown code fences
#     sql = sql.strip()

#     sql = re.sub(
#         r"^```(?:sql)?\s*",
#         "",
#         sql,
#         flags=re.IGNORECASE
#     )

#     sql = re.sub(
#         r"\s*```$",
#         "",
#         sql
#     )

#     return sql.strip()


# def is_safe_query(sql):

#     sql_clean = clean_sql(sql).upper()

#     # Query must start with SELECT
#     if not sql_clean.startswith("SELECT"):
#         return False

#     forbidden = [
#         "INSERT",
#         "UPDATE",
#         "DELETE",
#         "DROP",
#         "ALTER",
#         "TRUNCATE",
#         "CREATE",
#         "GRANT",
#         "REVOKE"
#     ]

#     for keyword in forbidden:

#         if re.search(
#             rf"\b{keyword}\b",
#             sql_clean
#         ):
#             return False

#     return True


# def run_query(sql):

#     sql = clean_sql(sql)

#     if not is_safe_query(sql):

#         raise ValueError(
#             "Unsafe SQL query blocked."
#         )

#     return pd.read_sql(
#         sql,
#         engine
#     )



# if __name__ == "__main__":

#     safe_sql = """
#     ```sql
#     SELECT *
#     FROM orders
#     LIMIT 5;
#     ```
#     """

#     dangerous_sql = """
#     DROP TABLE orders;
#     """

#     print("Safe query test:")
#     print(is_safe_query(safe_sql))

#     print("\nDangerous query test:")
#     print(is_safe_query(dangerous_sql))


# ==============================================Secure - levels ===============================================



import re

from sqlalchemy import text

# from src.database import engine
from src.database import readonly_engine


# Maximum number of rows returned by an AI-generated query
MAX_ROWS = 1000

# Maximum execution time for one SQL query
STATEMENT_TIMEOUT_MS = 10000


# SQL commands that are NOT allowed
BLOCKED_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "MERGE",
    "CALL",
    "COPY",
    "VACUUM",
    "ANALYZE",
    "COMMENT",
    "REINDEX",
    "REFRESH",
]


def clean_sql(sql):
    """
    Remove common Markdown code fences that an LLM may return.
    """

    if not sql:
        raise ValueError("SQL query is empty.")

    sql = sql.strip()

    # Remove ```sql ... ```
    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()


def remove_strings_and_comments(sql):
    """
    Remove quoted strings and SQL comments before checking
    dangerous keywords.

    This prevents words inside a normal string such as
    'delete' from being treated as SQL commands.
    """

    # Remove single-line comments
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)

    # Remove block comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)

    # Remove single-quoted strings
    sql = re.sub(r"'(?:''|[^'])*'", "''", sql)

    # Remove double-quoted identifiers
    sql = re.sub(r'"(?:""|[^"])*"', '""', sql)

    return sql


def validate_sql(sql):
    """
    Validate AI-generated SQL before sending it to PostgreSQL.
    """

    sql = clean_sql(sql)

    if not sql:
        raise ValueError("SQL query is empty.")

    # Remove final semicolon
    sql_without_final_semicolon = sql.rstrip().rstrip(";").strip()

    # Multiple SQL statements are not allowed.
    if ";" in sql_without_final_semicolon:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    # Remove strings/comments for keyword inspection
    check_sql = remove_strings_and_comments(
        sql_without_final_semicolon
    )

    # Only SELECT or WITH queries are allowed.
    if not re.match(
        r"^(SELECT|WITH)\b",
        check_sql,
        flags=re.IGNORECASE
    ):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # Block dangerous SQL operations.
    for keyword in BLOCKED_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            check_sql,
            flags=re.IGNORECASE
        ):
            raise ValueError(
                f"Blocked SQL operation detected: {keyword}"
            )

    # Block row-locking queries.
    if re.search(
        r"\bFOR\s+(UPDATE|NO\s+KEY\s+UPDATE|SHARE|KEY\s+SHARE)\b",
        check_sql,
        flags=re.IGNORECASE
    ):
        raise ValueError(
            "Row-locking queries are not allowed."
        )

    return sql_without_final_semicolon


def enforce_limit(sql):
    """
    Ensure AI-generated SELECT queries cannot return
    an unlimited number of rows.

    If no LIMIT exists, add LIMIT 1000.

    If LIMIT exists with a value larger than MAX_ROWS,
    reduce it to MAX_ROWS.
    """

    # Check whether LIMIT already exists
    limit_match = re.search(
        r"\bLIMIT\s+(\d+)\b",
        sql,
        flags=re.IGNORECASE
    )

    if limit_match:

        current_limit = int(limit_match.group(1))

        if current_limit > MAX_ROWS:

            sql = re.sub(
                r"\bLIMIT\s+\d+\b",
                f"LIMIT {MAX_ROWS}",
                sql,
                count=1,
                flags=re.IGNORECASE
            )

        return sql

    # No LIMIT -> add one
    return f"{sql}\nLIMIT {MAX_ROWS}"


def run_query(sql):
    """
    Validate and safely execute an AI-generated SQL query.
    """

    # -----------------------------------
    # Step 1: Validate SQL
    # -----------------------------------

    validated_sql = validate_sql(sql)

    # -----------------------------------
    # Step 2: Enforce row limit
    # -----------------------------------

    safe_sql = enforce_limit(validated_sql)

    # -----------------------------------
    # Step 3: Execute with timeout
    # -----------------------------------

    try:

        # with engine.connect() as connection:
        with readonly_engine.connect() as connection:

            # PostgreSQL statement timeout
            connection.execute(
                text(
                    f"SET statement_timeout = {STATEMENT_TIMEOUT_MS}"
                )
            )

            result = connection.execute(
                text(safe_sql)
            )

            rows = result.fetchall()

            columns = result.keys()

        # Convert result into pandas DataFrame
        import pandas as pd

        return pd.DataFrame(
            rows,
            columns=columns
        )

    except Exception as e:

        raise RuntimeError(
            f"SQL execution failed: {e}"
        ) from e