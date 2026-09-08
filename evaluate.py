import pandas as pd

from src.text_to_sql import generate_sql
from src.query_validator import run_query


# -----------------------------------
# 1. Load evaluation questions
# -----------------------------------

df = pd.read_csv("evaluation_queries.csv")

print(f"Loaded {len(df)} evaluation questions.")


# -----------------------------------
# 2. Store evaluation results
# -----------------------------------

results = []


# -----------------------------------
# 3. Test each question
# -----------------------------------

for index, row in df.iterrows():

    question_id = row["id"]
    difficulty = row["difficulty"]
    question = row["question"]

    print("\n" + "=" * 70)
    print(f"Question {question_id}")
    print(f"Difficulty: {difficulty}")
    print(f"Question: {question}")

    try:

        # Generate SQL using Gemini
        sql = generate_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        # Execute generated SQL
        result = run_query(sql)

        print("\nSQL executed successfully.")
        print(f"Rows returned: {len(result)}")

        results.append({
            "id": question_id,
            "difficulty": difficulty,
            "question": question,
            "sql": sql,
            "status": "success",
            "rows_returned": len(result),
            "error": ""
        })

    except Exception as e:

        print("\nSQL execution failed.")
        print(f"Error: {e}")

        results.append({
            "id": question_id,
            "difficulty": difficulty,
            "question": question,
            "sql": sql if "sql" in locals() else "",
            "status": "failed",
            "rows_returned": 0,
            "error": str(e)
        })


# -----------------------------------
# 4. Convert results to DataFrame
# -----------------------------------

results_df = pd.DataFrame(results)


# -----------------------------------
# 5. Calculate execution accuracy
# -----------------------------------

total_questions = len(results_df)

successful_questions = (
    results_df["status"] == "success"
).sum()

accuracy = (
    successful_questions / total_questions
) * 100


# -----------------------------------
# 6. Print final accuracy
# -----------------------------------

print("\n")
print("=" * 70)
print("TEXT-TO-SQL EVALUATION")
print("=" * 70)

print(f"Total questions: {total_questions}")
print(f"Successful SQL queries: {successful_questions}")
print(f"Failed SQL queries: {total_questions - successful_questions}")
print(f"Execution accuracy: {accuracy:.2f}%")


# -----------------------------------
# 7. Accuracy by difficulty
# -----------------------------------

print("\nAccuracy by difficulty:")

difficulty_accuracy = (
    results_df
    .groupby("difficulty")["status"]
    .apply(lambda x: (x == "success").mean() * 100)
)

print(difficulty_accuracy)


# -----------------------------------
# 8. Save detailed evaluation
# -----------------------------------

results_df.to_csv(
    "evaluation_results.csv",
    index=False
)

print("\nDetailed results saved to:")
print("evaluation_results.csv")