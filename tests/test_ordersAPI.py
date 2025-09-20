#!/usr/bin/env python3
import unittest
import requests

BASE_URL = "http://localhost:5000"


class TestOrdersAPI(unittest.TestCase):
    product_id = None
    order_id = None
    user_id = None

    @classmethod
    def setUpClass(cls):
        """Create a test user and product for orders"""
        cls.new_user = {
            "first_name": "Order",
            "last_name": "Tester",
            "username": "ordertester",
            "email": "ordertester@example.com",
            "password": "securepass123"
        }
        res_user = requests.post(f"{BASE_URL}/users/create", json=cls.new_user)
        res_user.raise_for_status()
        results = requests.get(f"{BASE_URL}/users").json()
        for result in results:
            if result.get("email") == cls.new_user["email"]:
                cls.user_id = result["id"]
                break

        cls.new_product = {
            "name": "Test Product",
            "volume": 1000,
            "price": 100
        }
        res_prod = requests.post(f"{BASE_URL}/products/create", json=cls.new_product)
        res_prod.raise_for_status()
        results = requests.get(f"{BASE_URL}/products").json()
        for result in results:
            if result.get("name") == cls.new_product["name"]:
                cls.product_id = result["id"]
                break

    def test_01_create_order(self):
        """Test creating a new order with items"""
        order_data = {
            "user_id": self.user_id,
            "items": {self.product_id: 3}
        }
        res = requests.post(f"{BASE_URL}/orders/create", json=order_data)
        self.assertEqual(res.status_code, 201)

        results = requests.get(f"{BASE_URL}/orders").json()
        for result in results:
            if self.user_id == result.get("user_id"):
                self.__class__.order_id = result["id"]
                break

        self.assertIsNotNone(self.order_id)

    def test_02_get_order(self):
        """Retrieve order by ID"""
        res = requests.get(f"{BASE_URL}/orders/{self.order_id}")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], self.order_id)

    def test_03_get_all_orders(self):
        """Retrieve all orders"""
        res = requests.get(f"{BASE_URL}/orders")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_05_get_order_items(self):
        """Retrieve items in an order"""
        res = requests.get(f"{BASE_URL}/orders/{self.order_id}/items")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_06_delete_order(self):
        """Delete an order"""
        res = requests.delete(f"{BASE_URL}/orders/{self.order_id}")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json().get("success"), "OK")

    @classmethod
    def tearDownClass(cls):
        """Clean up test data: product + user"""
        if cls.order_id:
            requests.delete(f"{BASE_URL}/orders/{cls.order_id}")
        if cls.product_id:
            requests.delete(f"{BASE_URL}/products/{cls.product_id}")
        if cls.user_id:
            requests.delete(f"{BASE_URL}/users/{cls.user_id}")


if __name__ == "__main__":
    unittest.main()
