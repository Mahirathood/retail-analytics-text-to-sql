# Retail Analytics + Text-to-SQL

An AI-powered retail analytics application that allows users to ask business questions in natural language and receive SQL-driven insights from a PostgreSQL database.

The project combines **Data Analytics, SQL, Python, Generative AI, and Business Intelligence** into a single end-to-end analytics solution.

---

## 1. Problem

Business users often need data insights but may not know SQL.

Traditional analytics workflows require users to:

1. Understand the database structure
2. Write SQL queries
3. Execute queries
4. Analyze the results
5. Create visualizations
6. Interpret the business meaning

This creates a barrier for non-technical users who want quick access to business insights.

---

## 2. Solution

Developed a natural-language retail analytics assistant that converts business questions into PostgreSQL queries using a Large Language Model (LLM).

Users can ask questions such as:

> "What is the total revenue?"

> "Which states generate the highest revenue?"

> "What is the average order value?"

> "How many orders were delivered?"

The application:

1. Understands the user's question
2. Provides database schema context to the LLM
3. Generates PostgreSQL SQL
4. Validates the generated SQL
5. Executes the query using a read-only database connection
6. Returns the result using Pandas
7. Generates a natural-language explanation
8. Displays analytics and visualizations through Streamlit

---

## 3. Architecture

```text
User
  |
  v
Streamlit Application
  |
  v
Conversation History
  |
  v
Gemini LLM
  |
  v
Schema Context
  |
  v
SQL Generation
  |
  v
SQL Validator
  |
  v
Read-Only PostgreSQL
  |
  v
Pandas DataFrame
  |
  +--------------------+
  |                    |
  v                    v
Visualization      LLM Summary
  |                    |
  +---------+----------+
            |
            v
        Business Insight

4. Dataset

This project uses the Olist Brazilian E-Commerce Public Dataset.

The dataset contains information about Brazilian e-commerce operations, including:

    Customers

    Orders

    Order items

    Products

    Payments

    Reviews

    Sellers

    Geolocation

    Product categories

The raw dataset is not included in this repository.
5. Key Features
5.1 Executive Dashboard

The application provides an executive-level dashboard with business KPIs including:

    Total Revenue

    Total Orders

    Total Customers

    Average Order Value

    Average Product Price

    Average Review Score

    Delivered Orders

    Delivery Rate

The dashboard also provides interactive filters such as:

    Year

    Order Status

And visualizations including:

    Revenue Trend

    Revenue by State

    Payment Type Distribution

    Top Product Categories

    Order Status Distribution

5.2 Natural Language → SQL

Users can ask business questions using normal language.

Example:

Which states generate the highest revenue?

The system generates an appropriate PostgreSQL query and executes it against the retail database.
5.3 Schema-Aware SQL Generation

The LLM receives information about the database schema before generating SQL.

This helps the model understand:

    Available tables

    Column names

    Relationships

    Data structure

This reduces incorrect table and column references.
5.4 SQL Security

Generated SQL is validated before execution.

The application allows only:

SELECT
WITH

queries.

The validator blocks potentially destructive operations such as:

INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
MERGE
CALL
COPY
VACUUM
ANALYZE
COMMENT
REINDEX
REFRESH

The system also:

    Blocks multiple SQL statements

    Blocks row-locking queries

    Enforces a maximum result size of 1,000 rows

    Applies a database statement timeout

    Uses a dedicated read-only PostgreSQL role for application queries

5.5 Conversation History

The application maintains previous user questions and assistant responses.

This allows follow-up questions to use the context of the previous conversation.

Example:

User:
What was the total revenue in 2017?

User:
What about 2018?

The second question can use the context from the previous interaction.
5.6 Automatic SQL Retry

If the generated SQL fails during execution, the application attempts to generate a corrected SQL query using:

    Original business question

    Failed SQL query

    Database error message

The corrected SQL is validated again before execution.

This creates a self-correction workflow:

Question
   |
   v
Generate SQL
   |
   v
Validate SQL
   |
   v
Execute SQL
   |
   +---- Success ----> Result
   |
   +---- Error ------> Fix SQL
                         |
                         v
                    Validate Again
                         |
                         v
                      Execute

6. Business KPIs

The project calculates important retail business metrics such as:
KPI	Description
Total Revenue	Total customer payment/revenue amount
Total Orders	Number of orders
Total Customers	Number of customers
Average Order Value	Average revenue per order
Average Product Price	Average product item price
Average Review Score	Average customer review score
Delivered Orders	Number of successfully delivered orders
Delivery Rate	Percentage of orders delivered

These metrics provide an executive-level view of business performance.
7. Technology Stack
Technology	Purpose
Python	Data processing and application development
Pandas	Data analysis and DataFrame operations
PostgreSQL	Relational database
SQLAlchemy	Database connectivity
Gemini API	Natural-language understanding and SQL generation
Streamlit	Interactive web application
Plotly	Data visualization
python-dotenv	Environment variable management
Git	Version control
GitHub	Source code hosting
8. Project Structure

Retail Analytics + Text-to-SQL/
│
├── app.py
├── evaluate.py
├── evaluation_queries.csv
├── load_data.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── data_cleaning.py
│   ├── data_quality.py
│   ├── inspect_data.py
│   ├── metrics.py
│   ├── query_validator.py
│   ├── schema.py
│   ├── text_to_sql.py
│   └── test_pipeline.py
│
├── test_metrics.py
├── test_executive_metrics.py
├── test_security.py
├── test_ai_security.py
├── test_queries.py
├── test_readonly.py
├── test_readonly_query.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt

    .env, raw data, processed data, and the virtual environment are excluded from GitHub using .gitignore.

9. Data Preparation

The project includes a data-cleaning pipeline before loading data into PostgreSQL.

The cleaning process includes:

    Loading raw CSV files

    Converting order date/time columns

    Handling missing product categories

    Preserving other missing values where appropriate

    Saving cleaned datasets into data/processed/

The cleaned datasets are then loaded into PostgreSQL.
10. Database

The application uses PostgreSQL hosted on Supabase.

The database contains analytical tables such as:

orders
customers
order_items
products
payments
order_reviews

The application uses a separate read-only database role for executing generated SQL queries.

This provides an additional security layer between the AI-generated SQL and the production database.
11. How the Application Works
Step 1 — User Question

The user enters a natural-language business question.

Which states generate the highest revenue?

Step 2 — Schema Retrieval

The application provides the database schema to the LLM.
Step 3 — SQL Generation

The Gemini model generates PostgreSQL SQL.
Step 4 — SQL Validation

The generated SQL is checked for unsafe operations.

Only read-only queries are allowed.
Step 5 — Query Execution

The validated query is executed using the read-only PostgreSQL connection.
Step 6 — Data Processing

The query result is converted into a Pandas DataFrame.
Step 7 — Visualization

If appropriate, the result can be visualized using Plotly.
Step 8 — Business Explanation

The LLM summarizes the result in natural language.
12. Environment Setup

Create a .env file in the project root:

DATABASE_URL=your_write_database_connection
READONLY_DATABASE_URL=your_readonly_database_connection
GEMINI_API_KEY=your_gemini_api_key

Do not commit .env to GitHub.
13. Installation

Clone the repository and navigate into the project:

git clone https://github.com/Mahirathood/retail-analytics-text-to-sql.git

cd retail-analytics-text-to-sql

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

14. Load the Data

After configuring the database connection and preparing the processed datasets:

python load_data.py

This loads the datasets into PostgreSQL.
15. Run the Application

Start the Streamlit application:

streamlit run app.py

The application opens in the browser and provides:

    Executive dashboard

    Natural-language analytics

    SQL generation

    Query execution

    Visualizations

    Result explanations

    Conversation history

16. Example Business Questions

The application can answer questions such as:

What is the total revenue?

How many orders were delivered?

What is the average order value?

Which states generate the highest revenue?

What are the top product categories?

What payment types are most commonly used?

How many orders were canceled?

What is the average customer review score?

How did revenue change over time?

17. Testing

The project includes tests for different parts of the system.

Examples include:
SQL Security Testing

python test_security.py

Tests include:

    SELECT queries

    INSERT blocking

    UPDATE blocking

    DELETE blocking

    DROP blocking

    ALTER blocking

    Multiple-statement blocking

    LIMIT enforcement

Read-Only Database Testing

python test_readonly.py

This verifies that the application database connection cannot modify data.
Query Execution Testing

python test_readonly_query.py

This verifies that safe analytical SELECT queries can execute successfully using the read-only connection.
Metrics Testing

python test_metrics.py

Executive Metrics Testing

python test_executive_metrics.py

18. Evaluation

A separate evaluation dataset containing 25 business questions is included in:

evaluation_queries.csv

The evaluation framework is implemented in:

evaluate.py

The evaluation is designed to measure the accuracy of generated SQL against expected analytical queries.

    Evaluation accuracy is intentionally not reported here until the full 25-question benchmark can be completed successfully. This avoids presenting an unverified accuracy percentage.

19. Security Design

Security was treated as an important part of the Text-to-SQL architecture.

The system uses multiple protection layers:

LLM
 |
 v
SQL Validator
 |
 +--> Block unsafe SQL
 |
 +--> Allow SELECT/WITH only
 |
 +--> Enforce LIMIT
 |
 +--> Block multiple statements
 |
 +--> Block row locking
 |
 +--> Apply statement timeout
 |
 v
Read-Only PostgreSQL Role
 |
 v
Database

This ensures that AI-generated SQL cannot directly perform normal write or destructive database operations through the application connection.
20. Data Analyst Perspective

This project demonstrates practical skills relevant to a Data Analyst role:
SQL

    SELECT queries

    Aggregations

    GROUP BY

    ORDER BY

    JOIN operations

    Business metrics

    Analytical querying

Python

    Pandas

    Data cleaning

    Data validation

    Database interaction

    Automation

Data Visualization

    KPI dashboards

    Revenue trends

    Category analysis

    Geographic analysis

    Payment analysis

    Order-status analysis

Business Analytics

    Revenue analysis

    Customer analysis

    Order analysis

    Product analysis

    Payment analysis

    Delivery performance

    Review analysis

Generative AI

    Natural-language analytics

    Text-to-SQL

    Schema-aware prompting

    SQL correction

    Result summarization

    Conversation context

Data Engineering / Database

    PostgreSQL

    SQLAlchemy

    Data loading

    Database roles

    Read-only access

    Query security

21. My Role
Data Analyst / Analytics Developer

Responsibilities demonstrated through this project:

    Designed the retail analytics workflow

    Cleaned and prepared datasets

    Loaded data into PostgreSQL

    Developed analytical SQL queries

    Built business KPIs

    Created an executive dashboard

    Developed natural-language Text-to-SQL functionality

    Implemented SQL validation and security controls

    Added automated SQL retry logic

    Added conversation history

    Built an evaluation framework

    Developed automated tests

    Managed the project using Git and GitHub

22. Future Improvements

Potential future improvements include:

    Improve Text-to-SQL accuracy

    Expand the evaluation benchmark

    Add more complex analytical questions

    Improve SQL generation using stronger schema relationships

    Add more advanced visualizations

    Add role-based access control

    Add query caching

    Add query performance monitoring

    Add additional business dashboards

    Deploy the application to a cloud platform

    Improve production observability

23. Project Outcome

This project demonstrates an end-to-end analytics workflow:

Raw Data
   ↓
Data Cleaning
   ↓
PostgreSQL
   ↓
Analytical SQL
   ↓
Business Metrics
   ↓
Executive Dashboard
   ↓
Generative AI
   ↓
Natural Language → SQL
   ↓
Secure Query Execution
   ↓
Business Insights

The project combines traditional data analytics with Generative AI to make retail data more accessible to non-technical users.
24. Author

Mahendar Bhukya

GitHub:

https://github.com/Mahirathood
25. License

This project is intended for educational, portfolio, and demonstration purposes.


### What I corrected from your version

Your original structure was **good**, so I did **not** replace it completely. I kept your main sections and added only what makes the project stronger and more accurate:

| Your version | Final version |
|---|---|
| Problem | ✅ Kept |
| Solution | ✅ Kept |
| Architecture | ✅ Expanded |
| Dataset | ✅ Kept |
| Technologies | ✅ Kept |
| 25-question evaluation | ✅ Kept, but no unverified 92% |
| Project structure | ✅ Corrected to match actual files |
| Executive dashboard | ➕ Added |
| Text-to-SQL | ➕ Added |
| Conversation history | ➕ Added |
| Automatic SQL retry | ➕ Added |
| SQL security | ➕ Added |
| Database/read-only role | ➕ Added |
| Testing | ➕ Added |
| Data Analyst perspective | ➕ Added |
| My Role | ➕ Added |
| Future improvements | ➕ Added |
| 11-day development plan | ❌ Removed from README |

**Most important correction:** don't put `23/25 = 92%` in the README yet. Your evaluation framework has 25 questions, but the complete benchmark hasn't successfully finished because of the Gemini quota issue. Claiming 92% without the completed run would weaken the credibility of the project.

This version is the one I recommend using as your **final portfolio README**.