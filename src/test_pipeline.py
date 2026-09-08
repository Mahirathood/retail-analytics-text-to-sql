from src.text_to_sql import generate_sql
from src.query_validator import run_query
from src.database import engine


def run_pipeline(question):

    print("\n" + "=" * 60)
    print("TEXT-TO-SQL PIPELINE")
    print("=" * 60)

    # Step 1: Generate SQL
    print("\n1. USER QUESTION:")
    print(question)

    sql = generate_sql(question)

    print("\n2. GENERATED SQL:")
    print(sql)

    # Step 2: Validate and execute SQL
    print("\n3. EXECUTING QUERY...")

    result = run_query(
        sql,
        engine
    )

    # Step 3: Display result
    print("\n4. QUERY RESULT:")
    print(result)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":

    question = "What are the top 10 product categories by revenue?"

    run_pipeline(question)