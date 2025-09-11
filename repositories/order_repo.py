#!/usr/bin/env python3
"""Manage order creation and completion"""

from models.order import Order
from models.order_item import OrderItem
from models import storage


class OrderRepository:
    """Order manipulations"""

    def create_order(self, user_id, items):
        if not items or not isinstance(items, dict):
            raise ValueError("Order must be a dict")
        order = Order(user_id=user_id)
        order.save()
        storage.save()
        for product_id, quantity in items.items():
            new_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity)
            new_item.save()
        storage.save()
        return order

    def delete_order(self, order_id):
        order = storage.get(Order, order_id)
        storage.delete(order)
