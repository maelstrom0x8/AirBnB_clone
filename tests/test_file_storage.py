#!/usr/bin/env python3
"""File Storage testing module"""
import unittest
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel  # Import your FileStorage class


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        # This method will run before each test case
        self.storage = FileStorage()

    def tearDown(self):
        # This method will run after each test case
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_file_path(self):
        f1 = FileStorage()
        with self.assertRaises(AttributeError):
            f1.__file_path

    def test_file_object(self):
        f1 = FileStorage()
        with self.assertRaises(AttributeError):
            f1.__objects

    def test_all(self):
        """Test the 'all' method of FileStorage"""
        self.assertEqual(FileStorage._FileStorage__objects, self.storage.all())

    def test_new(self):
        """Test the 'new' method of FileStorage"""
        b1 = BaseModel()
        self.storage.new(b1)

        # Assert: Check if the object was added correctly
        tmp = {}
        for key, value in self.storage.all().items():
            tmp[key] = value.to_dict()
        self.assertIn(f"{b1.__class__.__name__}.{b1.id}", tmp)


if __name__ == '__main__':
    unittest.main()
