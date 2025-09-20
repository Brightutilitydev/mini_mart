#!/usr/bin/env python3
import unittest
import requests

BASE_URL = "http://localhost:5000/users"

class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        """Runs once before all tests: create a new user"""
        self.new_user = {
            "first_name": "John",
            "last_name": "Doe",
            "other_name": "Tester",
            "username": "johndoe_unittest",
            "email": "johndoe_unittest@example.com",
            "address": "123 Testing Street",
            "password": "securepassword"
        }

        res = requests.post(f"{BASE_URL}/create", json=self.new_user)
        self.assert_status(res, [201, 400])  # 400 if duplicate
        self.created_id = None

        res = requests.get(BASE_URL)
        for u in res.json():
            if u["username"] == self.new_user["username"]:
                self.created_id = u["id"]
                break

    def tearDown(self):
        """Runs once after all tests: clean up user"""
        if self.created_id:
            requests.delete(f"{BASE_URL}/{self.created_id}")

    def assert_status(self, res, expected_statuses):
        self.assertIn(res.status_code, expected_statuses, f"Got {res.status_code}, body={res.text}")
        return

    def test_get_all_users(self):
        res = requests.get(BASE_URL)
        self.assertEqual(res.status_code, 200)
        users = res.json()
        self.assertIsInstance(users, list)

    def test_get_user_by_id(self):
        res = requests.get(f"{BASE_URL}/{self.created_id}")
        self.assertEqual(res.status_code, 200)
        user = res.json()
        self.assertEqual(user["username"], self.new_user["username"])

    def test_update_user(self):
        update_data = {
            "id": self.created_id,
            "address": "456 Updated Lane",
            "first_name": "Johnny"
        }
        res = requests.put(f"{BASE_URL}/update", json=update_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("success", res.json())

        # confirm update
        res = requests.get(f"{BASE_URL}/{self.created_id}")
        self.assertEqual(res.json()["first_name"], "Johnny")

    def test_delete_user(self):
        # delete
        res = requests.delete(f"{BASE_URL}/{self.created_id}")
        self.assert_status(res, [200, 201, 404])

        # confirm deletion
        res = requests.get(f"{BASE_URL}/{self.created_id}")
        self.assertIn(res.status_code, [404, 400])
        body = res.json()
        self.assertIn("error", body)

if __name__ == "__main__":
    unittest.main(verbosity=2)
