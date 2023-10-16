#!/usr/bin/env python3
"""BaseModel testing module"""
import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """A test case class for Base Model"""

    def setUp(self):
        """
        Set up the test case by initializing a BaseModel instance.
        """
        self.model = BaseModel()

    def test_base_model_creation(self):
        """Test if the BaseModel instance is created successfully."""
        self.assertIsInstance(self.model, BaseModel)

    def test_id_generation(self):
        """
        Test the generation of unique IDs for different BaseModel instances.
        """
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_created_at_exists(self):
        """Test if 'created_at' attribute exists in the BaseModel instance."""
        self.assertTrue(hasattr(self.model, "created_at"))

    def test_updated_at_exists(self):
        """Test if 'updated_at' attribute exists in the BaseModel instance"""
        self.assertTrue(hasattr(self.model, "updated_at"))

    def test_created_at_type(self):
        """Test if 'created_at' is a valid date"""
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_type(self):
        """Test if 'created_at' is a valid date"""
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str_method(self):
        """
        Test the string representation of the BaseModel instance.
        """
        string = str(self.model)
        self.assertIn("[BaseModel] ({})".format(self.model.id), string)
        self.assertIn("'created_at': datetime.datetime", string)
        self.assertIn("'updated_at': datetime.datetime", string)

    def test_save_method(self):
        """
        Test the 'save' method to ensure 'updated_at' attribute changes.
        """
        initial_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(initial_updated_at, self.model.updated_at)

    def test_to_dict_method(self):
        """
        Test the 'to_dict' method to verify the dictionary representation.
        """
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)
        self.assertIn("__class__", model_dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")


if __name__ == "__main__":
    unittest.main()
