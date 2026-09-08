from src.query_validator import run_query


def get_total_revenue():
    query = """
    SELECT
        SUM(price + freight_value) AS total_revenue
    FROM order_items;
    """

    result = run_query(query)

    return result.iloc[0]["total_revenue"]


def get_total_orders():
    query = """
    SELECT
        COUNT(*) AS total_orders
    FROM orders;
    """

    result = run_query(query)

    return result.iloc[0]["total_orders"]


def get_total_customers():
    query = """
    SELECT
        COUNT(*) AS total_customers
    FROM customers;
    """

    result = run_query(query)

    return result.iloc[0]["total_customers"]


def get_average_order_value():
    query = """
    SELECT
        AVG(order_total) AS average_order_value
    FROM (
        SELECT
            order_id,
            SUM(price + freight_value) AS order_total
        FROM order_items
        GROUP BY order_id
    ) AS order_totals;
    """

    result = run_query(query)

    return result.iloc[0]["average_order_value"]


def get_average_product_price():
    query = """
    SELECT
        AVG(price) AS average_product_price
    FROM order_items;
    """

    result = run_query(query)

    return result.iloc[0]["average_product_price"]


def get_average_review_score():
    query = """
    SELECT
        AVG(review_score) AS average_review_score
    FROM order_reviews;
    """

    result = run_query(query)

    return result.iloc[0]["average_review_score"]


def get_delivered_orders():
    query = """
    SELECT
        COUNT(*) AS delivered_orders
    FROM orders
    WHERE order_status = 'delivered';
    """

    result = run_query(query)

    return result.iloc[0]["delivered_orders"]


def get_delivery_rate():
    query = """
    SELECT
        100.0 *
        SUM(
            CASE
                WHEN order_status = 'delivered'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*) AS delivery_rate
    FROM orders;
    """

    result = run_query(query)

    return result.iloc[0]["delivery_rate"]


# def get_monthly_revenue():
#     query = """
#     SELECT
#         DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
#         SUM(oi.price + oi.freight_value) AS revenue
#     FROM orders o
#     JOIN order_items oi
#         ON o.order_id = oi.order_id
#     GROUP BY month
#     ORDER BY month;
#     """

#     return run_query(query)

def get_monthly_revenue():
    query = """
    SELECT
        DATE_TRUNC(
            'month',
            CAST(o.order_purchase_timestamp AS TIMESTAMP)
        ) AS month,
        SUM(oi.price + oi.freight_value) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY month
    ORDER BY month;
    """

    return run_query(query)


def get_revenue_by_state():
    query = """
    SELECT
        c.customer_state,
        SUM(oi.price + oi.freight_value) AS revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_state
    ORDER BY revenue DESC;
    """

    return run_query(query)


def get_top_categories():
    query = """
    SELECT
        COALESCE(p.product_category_name, 'unknown') AS category,
        SUM(oi.price + oi.freight_value) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY category
    ORDER BY revenue DESC
    LIMIT 10;
    """

    return run_query(query)

def get_revenue_by_payment_type():
    query = """
    SELECT
        p.payment_type,
        SUM(p.payment_value) AS revenue
    FROM payments p
    GROUP BY p.payment_type
    ORDER BY revenue DESC;
    """

    return run_query(query)


def get_orders_by_status():
    query = """
    SELECT
        order_status,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY order_status
    ORDER BY order_count DESC;
    """

    return run_query(query)

def get_available_years():
    query = """
    SELECT DISTINCT
        EXTRACT(
            YEAR FROM CAST(order_purchase_timestamp AS TIMESTAMP)
        ) AS year
    FROM orders
    WHERE order_purchase_timestamp IS NOT NULL
    ORDER BY year;
    """

    return run_query(query)


def get_filtered_monthly_revenue(year=None, order_status=None):
    query = """
    SELECT
        DATE_TRUNC(
            'month',
            CAST(o.order_purchase_timestamp AS TIMESTAMP)
        ) AS month,
        SUM(oi.price + oi.freight_value) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE 1=1
    """

    if year is not None:
        query += f"""
        AND EXTRACT(
            YEAR FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)
        ) = {int(year)}
        """

    if order_status != "All":
        query += f"""
        AND o.order_status = '{order_status}'
        """

    query += """
    GROUP BY month
    ORDER BY month;
    """

    return run_query(query)


def get_filtered_state_revenue(year=None, order_status=None):
    query = """
    SELECT
        c.customer_state,
        SUM(oi.price + oi.freight_value) AS revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE 1=1
    """

    if year is not None:
        query += f"""
        AND EXTRACT(
            YEAR FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)
        ) = {int(year)}
        """

    if order_status != "All":
        query += f"""
        AND o.order_status = '{order_status}'
        """

    query += """
    GROUP BY c.customer_state
    ORDER BY revenue DESC;
    """

    return run_query(query)


def get_filtered_payment_revenue(year=None, order_status=None):
    query = """
    SELECT
        p.payment_type,
        SUM(p.payment_value) AS revenue
    FROM payments p
    JOIN orders o
        ON p.order_id = o.order_id
    WHERE 1=1
    """

    if year is not None:
        query += f"""
        AND EXTRACT(
            YEAR FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)
        ) = {int(year)}
        """

    if order_status != "All":
        query += f"""
        AND o.order_status = '{order_status}'
        """

    query += """
    GROUP BY p.payment_type
    ORDER BY revenue DESC;
    """

    return run_query(query)