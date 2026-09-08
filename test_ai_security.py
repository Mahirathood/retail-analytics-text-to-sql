from src.text_to_sql import generate_sql
from src.query_validator import validate_sql, enforce_limit


questions = [
    "What are the top 5 product categories by revenue?",
    "Which state has the most customers?",
    "What is the average order value?",
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(question)

    try:

        # Generate SQL using Gemini
        sql = generate_sql(question)

        print("\nGENERATED SQL")
        print("-" * 70)
        print(sql)

        # Security validation
        validated_sql = validate_sql(sql)

        # Enforce LIMIT
        safe_sql = enforce_limit(validated_sql)

        print("\nSECURITY STATUS: SAFE")

        print("\nFINAL SQL")
        print("-" * 70)
        print(safe_sql)

    except Exception as e:

        print("\nSECURITY STATUS: BLOCKED / FAILED")
        print("Reason:", e)