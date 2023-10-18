#!/usr/bin/env python3

from io import StringIO
import os
import unittest
from unittest.mock import patch

from console import HBNBCommand, HBNBService


UUID_PATTERN = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}'

def clear_buffer(iofile: StringIO):
    iofile.seek(0)
    iofile.truncate(0)

class TestHBNBConsole(unittest.TestCase):

    def setUp(self) -> None:
        _path = 'file.json'
        if os.path.exists(_path):
            os.remove(_path)

    def tearDown(self) -> None:
        _path = 'file.json'
        if os.path.exists(_path):
            os.remove(_path)

    def test_create_fails_with_invalid_no_args(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().do_create('')
            self.assertEqual('** class name missing **', f.getvalue().strip())
    
    def test_create_command_is_case_sensitive(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().do_create('UseR')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

class TestHBNBService(unittest.TestCase):

    service: HBNBService = HBNBService()

    def setUp(self) -> None:
        _path = 'file.json'
        if os.path.exists(_path):
            os.remove(_path)

    def tearDown(self) -> None:
        _path = 'file.json'
        if os.path.exists(_path):
            os.remove(_path)

    def test_create(self):
        self.tearDown()
        _id = self.service.create('BaseModel')
        self.assertIsNotNone(_id)
        self.assertTrue(len(_id) > 0)
        self.assertRegex(_id, UUID_PATTERN)

    def test_fetch_created_model(self):
        a_id = self.service.create('Amenity')
        p_id = self.service.create('Place')

        amenity = self.service.fetch_model_by_id('Amenity', a_id)
        place = self.service.fetch_model_by_id('Place', p_id)

        self.assertIn(a_id, str(amenity))
        self.assertIn(p_id, str(place))
    
    @patch(target='sys.stdout', new_callable=StringIO)
    def test_count_after_delete(self, f: StringIO):
        id1 = self.service.create('User')
        self.service.create('User')

        self.assertEqual(2, self.service.fetch_model_count('User'))
        self.service.delete_model_by_id('User', id1)
        self.assertEqual(1, self.service.fetch_model_count('User'))
        self.assertNotIn(id1, self.service.fetch_all('User'))
        self.assertIsNone(self.service.fetch_model_by_id('User', id1))
        self.assertEqual('** no instance found **', f.getvalue().strip())


class TestCommandDoc(unittest.TestCase):

    def setUp(self) -> None:
        _path = 'file.json'
        if os.path.exists(_path):
            os.remove(_path)

    def tearDown(self) -> None:
        _path = 'file.json'
        if os.path.exists(_path):
            os.remove(_path)    

    def test_show_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(f.getvalue(), 'Prints a model instance\n')
    
    def test_quit_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertEqual('Quit command to exit the program', f.getvalue().strip())

    def test_EOF_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual('Handle EOF', f.getvalue().strip())

    def test_update_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual('Update model data', f.getvalue().strip())

    def test_create_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual('Create a new model', f.getvalue().strip())

    def test_all_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual('Lists all models of a class', f.getvalue().strip())

    def test_count_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help count")
            self.assertEqual('Prints the size of a model type', f.getvalue().strip())

    def test_destroy_doc(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual('Remove a model by id', f.getvalue().strip())



if __name__ == '__main__':
    unittest.main()
