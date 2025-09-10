#!/usr/bin/env python3
"""Populate database with sample users, products, and test orders"""

from models import storage
from models.user import User
from models.product import Product
from models.quantity import Quantity
from models.order import Order
from repositories.order_repo import OrderRepository

# --- Users ---
users = [
    User(first_name="Alice", last_name="Johnson", username="alicej", email="alice@example.com", address="123 Main St", password="hashed_pw1"),
    User(first_name="Bob", last_name="Smith", other_name="Lee", username="bobsmith", email="bob@example.com", address="456 Elm St", password="hashed_pw2"),
    User(first_name="Charlie", last_name="Brown", username="charlieb", email="charlie@example.com", address="789 Oak St", password="hashed_pw3"),
    User(first_name="Diana", last_name="Prince", other_name="W", username="dianap", email="diana@example.com", address="101 Pine St", password="hashed_pw4"),
    User(first_name="Ethan", last_name="Hunt", username="ethanh", email="ethan@example.com", address="202 Maple St", password="hashed_pw5"),
]

# --- Products ---
products = [
    Product(name="Milk", volume=1000),
    Product(name="Bread", volume=500),
    Product(name="Sugar", volume=2000),
    Product(name="Rice", volume=5000),
    Product(name="Salt", volume=1000),
    Product(name="Butter", volume=250),
    Product(name="Cheese", volume=300),
    Product(name="Eggs", volume=12),
    Product(name="Juice", volume=1500),
    Product(name="Water Bottle", volume=2000),
]

# Save them to DB
for u in users: u.save()
for p in products: p.save()
storage.save()

# --- Make an order ---
order_repo = OrderRepository()

# Example: user1 buys milk, cheese, sugar, salt
tinz_to_buy = {
    products[0].id: 25,   # milk
    products[6].id: 17,   # cheese
    products[2].id: 9,    # sugar
    products[4].id: 1     # salt
}

order = order_repo.create_order(users[0].id, tinz_to_buy)

print("\nOrder created:")
print(order)
print("Items in order:")
for q in order.quantities:
    print(f"- {q.product.name}: {q.quantity}")
print(f"Username of orderer: {order.user.username}")


print("\n____all quantities before deletion_______")
print(storage.all(Quantity))
order.delete()
storage.save()
print("\n_______all quantities after deletion________")
print(storage.all(Quantity))
