from src.metrics import (
    get_revenue_by_payment_type,
    get_orders_by_status
)


print("Revenue by Payment Type:")
print(
    get_revenue_by_payment_type()
)


print("\nOrders by Status:")
print(
    get_orders_by_status()
)