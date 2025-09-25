#!/usr/bin/env python3
"""Unittests for BaseModel"""

import unittest
import uuid
import inspect
import pycodestyle
from unittest.mock import patch, MagicMock
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test suite for BaseModel"""

    def setUp(self):
        """Run before each test"""
        self.obj = BaseModel()


    def test_module_docstring(self):
        """Module has a docstring"""
        import models.base_model as bm
        self.assertIsNotNone(bm.__doc__)
        self.assertTrue(len(bm.__doc__) > 10)

    def test_class_docstring(self):
        """Class BaseModel has a docstring"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertTrue(len(BaseModel.__doc__) > 10)

    def test_methods_docstrings(self):
        """All public methods have docstrings"""
        for name, func in inspect.getmembers(BaseModel, inspect.isfunction):
            self.assertIsNotNone(func.__doc__, f"{name} has no docstring")


    def test_pep8_compliance(self):
        """Test that models/base_model.py is PEP8 compliant"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 errors found")


    def test_id_is_uuid(self):
        """id is a valid UUID string"""
        try:
            uuid.UUID(self.obj.id, version=4)
        except ValueError:
            self.fail("id is not a valid UUID4 string")

    def test_created_at_and_last_modified_are_datetime(self):
        """created_at and last_modified are datetime"""
        self.assertIsInstance(self.obj.created_at, datetime)
        self.assertIsInstance(self.obj.last_modified, datetime)


    def test_to_dict_contains_keys(self):
        """to_dict has required keys"""
        d = self.obj.to_dict()
        self.assertIn("id", d)
        self.assertIn("created_at", d)
        self.assertIn("last_modified", d)

    def test_to_dict_datetime_isoformat(self):
        """Datetime fields are converted to isoformat strings"""
        d = self.obj.to_dict()
        self.assertIsInstance(d["created_at"], str)
        self.assertIsInstance(d["last_modified"], str)
        self.assertIn("T", d["created_at"])  # looks like ISO


    @patch("models.storage")
    def test_save_calls_storage_add_and_save(self, mock_storage):
        """save() calls storage.add and storage.save with self"""
        self.obj.save()
        mock_storage.add.assert_called_once_with(self.obj)
        mock_storage.save.assert_called_once()

    @patch("models.storage")
    def test_save_updates_last_modified(self, mock_storage):
        """save() updates last_modified timestamp"""
        old_time = self.obj.last_modified
        self.obj.save()
        self.assertGreater(self.obj.last_modified, old_time)


    @patch("models.storage")
    def test_delete_calls_storage_delete(self, mock_storage):
        """delete() calls storage.delete with self"""
        self.obj.delete()
        mock_storage.delete.assert_called_once_with(self.obj)


    def test_repr_returns_readable_string(self):
        """__repr__ returns a formatted string"""
        rep = repr(self.obj)
        self.assertIn(self.obj.id, rep)
        self.assertIn("BaseModel", rep)


if __name__ == "__main__":
    unittest.main()
