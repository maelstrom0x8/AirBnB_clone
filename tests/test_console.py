#!/usr/bin/env python3

from io import StringIO
import unittest
from unittest.mock import patch

from console import HBNBCommand


class TestConsole(unittest.TestCase):

    def test_create_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(f.getvalue(), 'Prints a model instance\n')

    class TestCommandDoc(unittest.TestCase):
        pass

    class TestCommands(unittest.TestCase):
        pass
