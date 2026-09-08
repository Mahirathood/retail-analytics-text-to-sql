import streamlit as st
import plotly.express as px

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

    except Exception as e:

        st.warning(
            f"Unable to load order status analysis: {e}"
        )