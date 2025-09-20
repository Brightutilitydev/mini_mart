#!/usr/bin/env python3
"""
Unittest for Category API routes

Tests CRUD operations on the /categories endpoints:
    - Create category
    - Get all categories
    - Get single category
    - Update category
    - Delete category
"""

import unittest
import requests

BASE_URL = "http://localhost:5000/categories"


class TestCategoriesAPI(unittest.TestCase):
    """Test suite for categories API"""

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests: create a new category"""
        cls.new_category = {
            "name": "Groceries",
            "description": "Food and household items"
        }
        res = requests.post(f"{BASE_URL}/create", json=cls.new_category)
        cls.assert_status(res, [200, 201])
        # Fetch ID of created category from index
        all_cats = requests.get(BASE_URL)
        cls.category_id = None
        for cat in all_cats.json():
            if cat["name"] == cls.new_category["name"]:
                cls.category_id = cat["id"]
                break

    @staticmethod
    def assert_status(res, expected):
        """Helper: assert response status code"""
        if not isinstance(expected, list):
            expected = [expected]
        assert res.status_code in expected, f"Unexpected status: {res.status_code}, body: {res.text}"

    def test_01_get_all_categories(self):
        """GET /categories should return a list"""
        res = requests.get(BASE_URL)
        self.assert_status(res, 200)
        self.assertIsInstance(res.json(), list)

    def test_02_get_category(self):
        """GET /categories/<id> should return a single category"""
        res = requests.get(f"{BASE_URL}/{self.category_id}")
        self.assert_status(res, 200)
        data = res.json()
        self.assertEqual(data["id"], self.category_id)

    def test_03_update_category(self):
        """PUT /categories/update should update category fields"""
        update_data = {
            "id": self.category_id,
            "name": "Supermarket Items",
            "description": "Updated description"
        }
        res = requests.put(f"{BASE_URL}/update", json=update_data)
        self.assert_status(res, [200, 201])
        # Confirm update
        res = requests.get(f"{BASE_URL}/{self.category_id}")
        data = res.json()
        self.assertEqual(data["name"], "Supermarket Items")

    def test_04_delete_category(self):
        """DELETE /categories/<id> should remove category"""
        res = requests.delete(f"{BASE_URL}/{self.category_id}")
        self.assert_status(res, [200, 201])
        # Confirm deletion
        res = requests.get(f"{BASE_URL}/{self.category_id}")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
