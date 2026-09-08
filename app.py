import streamlit as st
import plotly.express as px
from numbers import Number

from src.text_to_sql import (
    generate_sql,
    summarize_result,
    fix_sql
)

from src.query_validator import run_query

from src.metrics import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_average_order_value,
    get_average_product_price,
    get_average_review_score,
    get_delivered_orders,
    get_delivery_rate,
    get_monthly_revenue,
    get_revenue_by_state,
    get_top_categories,
    get_revenue_by_payment_type,
    get_orders_by_status,
    get_available_years,
    get_filtered_monthly_revenue,
    get_filtered_state_revenue,
    get_filtered_payment_revenue
)


# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="Retail Analytics AI",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------
# Conversation history
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------
# Title
# -----------------------------------

st.title("📊 Retail Analytics AI")

st.write(
    "Ask questions about the e-commerce dataset "
    "using natural language."
)


# -----------------------------------
# Analyst KPI Dashboard
# -----------------------------------

st.header("📈 Business Overview")

try:

    total_revenue = get_total_revenue()
    total_orders = get_total_orders()
    total_customers = get_total_customers()
    average_order_value = get_average_order_value()
    average_review_score = get_average_review_score()
    delivery_rate = get_delivery_rate()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Revenue",
            f"R$ {total_revenue:,.2f}"
        )

    with col2:
        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col4:
        st.metric(
            "Average Order Value",
            f"R$ {average_order_value:,.2f}"
        )

    col5, col6 = st.columns(2)

    with col5:
        st.metric(
            "Delivery Rate",
            f"{delivery_rate:.2f}%"
        )

    with col6:
        st.metric(
            "Average Review Score",
            f"{average_review_score:.2f} / 5"
        )

except Exception as e:

    st.warning(
        f"Unable to load dashboard metrics: {e}"
    )


# -----------------------------------
# Dashboard Filters
# -----------------------------------

st.header("🔎 Dashboard Filters")

try:

    years_df = get_available_years()

    years = [
        int(year)
        for year in years_df["year"].tolist()
    ]

except Exception as e:

    st.warning(
        f"Unable to load years: {e}"
    )

    years = []


col1, col2 = st.columns(2)


with col1:

    selected_year = st.selectbox(
        "Year",
        ["All"] + years,
        index=0
    )


with col2:

    order_status_options = [
        "All",
        "delivered",
        "shipped",
        "canceled",
        "unavailable",
        "invoiced",
        "processing",
        "created",
        "approved"
    ]

    selected_status = st.selectbox(
        "Order Status",
        order_status_options,
        index=0
    )


# -----------------------------------
# Revenue Trend
# -----------------------------------

st.header("📈 Revenue Trend")

try:

    monthly_revenue = get_filtered_monthly_revenue(
        year=None if selected_year == "All" else selected_year,
        order_status=selected_status
    )

    if not monthly_revenue.empty:

        fig = px.line(
            monthly_revenue,
            x="month",
            y="revenue",
            title="Monthly Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No revenue data available for the selected filters."
        )

except Exception as e:

    st.warning(
        f"Unable to load revenue trend: {e}"
    )


# -----------------------------------
# Revenue by State
# -----------------------------------

st.header("🗺️ Revenue by State")

try:

    state_revenue = get_filtered_state_revenue(
        year=None if selected_year == "All" else selected_year,
        order_status=selected_status
    )

    if not state_revenue.empty:

        fig = px.bar(
            state_revenue.head(10),
            x="customer_state",
            y="revenue",
            title="Top 10 States by Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No state revenue data available for the selected filters."
        )

except Exception as e:

    st.warning(
        f"Unable to load state revenue: {e}"
    )


# -----------------------------------
# Top Product Categories
# -----------------------------------

st.header("🏆 Top Product Categories")

try:

    top_categories = get_top_categories()

    if not top_categories.empty:

        fig = px.bar(
            top_categories,
            x="category",
            y="revenue",
            title="Top 10 Product Categories by Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No product category data available."
        )

except Exception as e:

    st.warning(
        f"Unable to load product categories: {e}"
    )


# -----------------------------------
# Payment & Order Status Analysis
# -----------------------------------

st.header("💳 Payment & Order Status")

col1, col2 = st.columns(2)


# -----------------------------------
# Revenue by Payment Type
# -----------------------------------

with col1:

    st.subheader("Revenue by Payment Type")

    try:

        payment_revenue = get_filtered_payment_revenue(
            year=None if selected_year == "All" else selected_year,
            order_status=selected_status
        )

        if not payment_revenue.empty:

            fig = px.bar(
                payment_revenue,
                x="payment_type",
                y="revenue",
                title="Revenue by Payment Type"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No payment data available for the selected filters."
            )

    except Exception as e:

        st.warning(
            f"Unable to load payment analysis: {e}"
        )


# -----------------------------------
# Orders by Status
# -----------------------------------

with col2:

    st.subheader("Orders by Status")

    try:

        order_status = get_orders_by_status()

        if not order_status.empty:

            fig = px.pie(
                order_status,
                names="order_status",
                values="order_count",
                title="Order Status Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No order status data available."
            )

    except Exception as e:

        st.warning(
            f"Unable to load order status analysis: {e}"
        )


# -----------------------------------
# Conversation History
# -----------------------------------

if st.session_state.messages:

    st.header("💬 Conversation History")

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.write(
                f"👤 **You:** {message['content']}"
            )

        elif message["role"] == "assistant":

            st.write(
                f"🤖 **AI:** {message['content']}"
            )


# -----------------------------------
# Ask a Question
# -----------------------------------

st.header("🤖 Ask a Question")

examples = [
    "What is the total revenue?",
    "Which state has the most customers?",
    "What are the top 10 product categories by revenue?",
    "What is the average order value?",
    "Which payment type is used most often?",
    "Show monthly revenue for 2018."
]


selected_question = st.selectbox(
    "Choose an example question:",
    [""] + examples
)


question = st.text_input(
    "Or enter your own business question:",
    placeholder="What would you like to know?"
)


if not question and selected_question:

    question = selected_question


ask_button = st.button(
    "Ask AI"
)


# -----------------------------------
# Text-to-SQL Pipeline
# -----------------------------------

if ask_button and question:

    with st.spinner("Analyzing your question..."):

        try:

            # -----------------------------------
            # Generate SQL
            # -----------------------------------

            sql = generate_sql(
                question,
                st.session_state.messages
            )


            # -----------------------------------
            # Save User Question
            # -----------------------------------

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            # -----------------------------------
            # Generated SQL
            # -----------------------------------

            st.subheader("Generated SQL")

            st.code(
                sql,
                language="sql"
            )


            # -----------------------------------
            # Execute SQL
            # -----------------------------------

            try:

                result = run_query(sql)

            except Exception as first_error:

                st.warning(
                    "The generated SQL failed. "
                    "Attempting to correct the query..."
                )

                try:

                    corrected_sql = fix_sql(
                        question,
                        sql,
                        str(first_error)
                    )


                    st.subheader("Corrected SQL")

                    st.code(
                        corrected_sql,
                        language="sql"
                    )


                    result = run_query(
                        corrected_sql
                    )

                except Exception as second_error:

                    st.error(
                        f"SQL failed after retry: {second_error}"
                    )

                    st.stop()


            # -----------------------------------
            # Query Result
            # -----------------------------------

            st.subheader("Query Result")

            st.dataframe(
                result,
                use_container_width=True
            )


            # -----------------------------------
            # Visualization
            # -----------------------------------

            st.subheader("Visualization")


            # -----------------------------------
            # Empty result
            # -----------------------------------

            if result.empty:

                st.info(
                    "The query returned no results."
                )


            # -----------------------------------
            # Single-value result
            # -----------------------------------

            elif len(result.columns) == 1 and len(result) == 1:

                column_name = result.columns[0]

                value = result.iloc[0, 0]


                if isinstance(value, Number):

                    st.metric(
                        label=column_name.replace(
                            "_",
                            " "
                        ).title(),
                        value=f"{value:,.2f}"
                    )

                else:

                    st.metric(
                        label=column_name.replace(
                            "_",
                            " "
                        ).title(),
                        value=str(value)
                    )


            # -----------------------------------
            # Multi-row result
            # -----------------------------------

            elif len(result.columns) >= 2 and len(result) > 1:

                x_column = result.columns[0]


                # Find numeric columns
                numeric_columns = result.select_dtypes(
                    include="number"
                ).columns.tolist()


                # Remove x-axis column
                y_candidates = [
                    column
                    for column in numeric_columns
                    if column != x_column
                ]


                if y_candidates:

                    y_column = y_candidates[0]


                    # -----------------------------------
                    # Choose chart type
                    # -----------------------------------

                    if "month" in x_column.lower():

                        fig = px.line(
                            result,
                            x=x_column,
                            y=y_column,
                            markers=True,
                            title=(
                                f"{y_column.replace('_', ' ').title()} "
                                f"by Month"
                            )
                        )

                    else:

                        fig = px.bar(
                            result,
                            x=x_column,
                            y=y_column,
                            title=(
                                f"{y_column.replace('_', ' ').title()} "
                                f"by "
                                f"{x_column.replace('_', ' ').title()}"
                            )
                        )


                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


                else:

                    st.info(
                        "No suitable numeric column found "
                        "for visualization."
                    )


            # -----------------------------------
            # Unsupported result
            # -----------------------------------

            else:

                st.info(
                    "The result does not contain enough "
                    "data to create a visualization."
                )


            # -----------------------------------
            # Business Explanation
            # -----------------------------------

            explanation = summarize_result(
                question,
                result
            )


            st.subheader(
                "Business Explanation"
            )


            st.write(
                explanation
            )


            # -----------------------------------
            # Save Assistant Response
            # -----------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": explanation
                }
            )


        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )