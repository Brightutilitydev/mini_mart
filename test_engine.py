#!/usr/bin/env python3
"""Unit tests for Storage using a mocked User model"""

import unittest
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from models.engine import Storage

Base = declarative_base()


class MockUser(Base):
    """Simple mock user model for testing"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False)


class TestStorage(unittest.TestCase):
    def setUp(self):
        """Fresh in-memory DB before each test"""
        self.db = Storage("sqlite:///:memory:")
        Base.metadata.create_all(self.db._Storage__engine)
        self.db.reload()

    def tearDown(self):
        """Clean up session"""
        self.db.close()

    def test_add_and_get(self):
        user = MockUser(first_name="John", last_name="Doe", age=25)
        self.db.add(user)
        self.db.save()

        fetched = self.db.get(MockUser, user.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.first_name, "John")
        self.assertEqual(fetched.age, 25)

    def test_all_specific_model(self):
        u1 = MockUser(first_name="Alice", last_name="Smith", age=30)
        u2 = MockUser(first_name="Bob", last_name="Brown", age=40)
        self.db.add(u1)
        self.db.add(u2)
        self.db.save()

        users = self.db.all(MockUser)
        self.assertEqual(len(users), 2)
        self.assertSetEqual({u.first_name for u in users}, {"Alice", "Bob"})

    def test_all_without_model(self):
        """all(None) should return list of lists"""
        user = MockUser(first_name="Charlie", last_name="Test", age=50)
        self.db.add(user)
        self.db.save()

        result = self.db.all(base=Base)
        print(result)
        self.assertIsInstance(result, list)
        self.assertTrue(any(isinstance(sub, list) for sub in result))

    def test_delete(self):
        user = MockUser(first_name="Delete", last_name="Me", age=99)
        self.db.add(user)
        self.db.save()

        self.db.delete(user)
        self.db.save()

        gone = self.db.get(MockUser, user.id)
        self.assertIsNone(gone)

    def test_update_persistence(self):
        """Modifying an object and saving should persist changes"""
        user = MockUser(first_name="Temp", last_name="Guy", age=20)
        self.db.add(user)
        self.db.save()

        user.first_name = "Permanent"
        user.age = 21
        self.db.save()

        updated = self.db.get(MockUser, user.id)
        self.assertEqual(updated.first_name, "Permanent")
        self.assertEqual(updated.age, 21)

    def test_delete_none(self):
        """Deleting None should not raise an error"""
        try:
            self.db.delete(None)
            self.db.save()
        except Exception as e:
            self.fail(f"delete(None) raised {e}")

    def test_get_invalid_id(self):
        """Fetching with an invalid id should return None"""
        result = self.db.get(MockUser, 999)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
