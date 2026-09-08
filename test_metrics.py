from src.metrics import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_average_order_value,
    get_average_product_price,
    get_average_review_score,
    get_delivered_orders,
    get_delivery_rate
)


print("Total Revenue:")
print(get_total_revenue())

print("\nTotal Orders:")
print(get_total_orders())

print("\nTotal Customers:")
print(get_total_customers())

print("\nAverage Order Value:")
print(get_average_order_value())

print("\nAverage Product Price:")
print(get_average_product_price())

print("\nAverage Review Score:")
print(get_average_review_score())

print("\nDelivered Orders:")
print(get_delivered_orders())

print("\nDelivery Rate:")
print(get_delivery_rate())