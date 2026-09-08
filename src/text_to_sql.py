import os

from dotenv import load_dotenv
from google import genai

from src.schema import get_schema


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GEMINI API KEY
# =========================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY
)


# =========================================================
# FORMAT DATABASE SCHEMA
# =========================================================

def format_schema():

    rows = get_schema()

    schema_text = ""

    current_table = None

    for table_name, column_name, data_type in rows:

        if table_name != current_table:

            schema_text += (
                f"\nTable: {table_name}\n"
            )

            current_table = table_name

        schema_text += (
            f"- {column_name} ({data_type})\n"
        )

    return schema_text


# =========================================================
# GENERATE SQL
# =========================================================

def generate_sql(
    question,
    conversation_history=None
):

    schema = format_schema()

    history_text = ""

    if conversation_history:

        history_text = (
            "\nPREVIOUS CONVERSATION:\n"
        )

        for message in conversation_history:

            history_text += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

    prompt = f"""
You are a PostgreSQL SQL expert.

Your task is to convert a user's natural language
question into a PostgreSQL SQL query.

DATABASE SCHEMA:
{schema}

{history_text}

CURRENT USER QUESTION:
{question}

RULES:
1. Return only the SQL query.
2. Use only tables and columns that exist in the schema.
3. Use PostgreSQL syntax.
4. Do not create or modify data.
5. Do not use INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, GRANT, or REVOKE.
6. Return a SELECT query only.
7. If the current question refers to previous
   conversation, use the previous conversation
   to understand the context.
8. Add a reasonable LIMIT when returning detailed rows.

Return only SQL.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql = response.text.strip()

    return sql


# =========================================================
# FIX FAILED SQL
# =========================================================

def fix_sql(
    question,
    failed_sql,
    error_message
):

    schema = format_schema()

    prompt = f"""
You are a PostgreSQL SQL expert.

The SQL query generated for the user's question failed.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

FAILED SQL:
{failed_sql}

DATABASE ERROR:
{error_message}

Your task is to correct the SQL query.

RULES:
1. Return only the corrected SQL query.
2. Use only tables and columns that exist in the schema.
3. Use PostgreSQL syntax.
4. Do not create or modify data.
5. Do not use INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, GRANT, or REVOKE.
6. Return a SELECT query only.
7. Fix the problem described by the database error.
8. Add a reasonable LIMIT when returning detailed rows.

Return only SQL.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    corrected_sql = response.text.strip()

    return corrected_sql


# =========================================================
# SUMMARIZE QUERY RESULT
# =========================================================

def summarize_result(
    question,
    result_df
):

    result_text = (
        result_df
        .head(50)
        .to_string(index=False)
    )

    prompt = f"""
You are a business data analyst.

Business question:
{question}

SQL result:
{result_text}

Explain the result in 2-3 concise sentences.

RULES:
1. Use only information present in the SQL result.
2. Do not invent numbers, trends, causes, or explanations.
3. Mention the most important finding.
4. Keep the explanation simple and business-friendly.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    explanation = response.text.strip()

    return explanation