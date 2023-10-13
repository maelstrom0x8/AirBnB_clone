#!/usr/bin/env python3

"""
console.py - Entrypoint for AirBnB CLI application

This module provides the main entrypoint for the program. It
parses and handles the commands.

Classes:
    HBNBCommand: A command-line parser class.
"""

from datetime import datetime
import importlib
import sys
import cmd
from types import ModuleType
from models.base_model import BaseModel

from models.engine.file_storage import FileStorage


class AirBnBService:

    storage = FileStorage()

    def create(self, args):
        class_name = args
        _module_name = self.__get_module(args)
        b, module = self.__module_exists(_module_name)
        if b is False:
            print("** class doesn't exist **")
            return
        else:
            self.__save_instance(module, class_name, args)
            return

    def update_model_attribute(self, model, id, attr, value):
        _module_name = self.__get_module(model)
        b, module = self.__module_exists(_module_name)
        if b is False:
            print("** class doesn't exist **")
            return
        key = '.'.join([model, id])
        instance: BaseModel = self.storage.all().get(key, None)
        if instance is not None:
            instance.__setattr__(attr, value)
            instance.updated_at = datetime.now()
            print(instance)
            self.storage.all()[key] = instance
            self.storage.save()
        else:
            print('** no instance found **')
            return

    def delete_model_by_id(self, model, _id):
        _module_name = self.__get_module(model)
        b, _ = self.__module_exists(_module_name)
        if not b:
            print("** class doesn't exist **")
            return
        else:
            self.__delete_instance(model, _id)

    def fetch_model_by_id(self, model, id):
        key = '.'.join([model, id])
        _model = self.storage.all().get(key, None)
        if _model is None:
            print('** instance not found **')
            return
        print(_model)

    def fetch_all(self, model):
        _models = self.storage.all()
        for e in _models.values():
            if e.__class__.__name__ == model:
                print(e)
        return

    def __get_module(self, name):
        return 'base_model' if name == 'BaseModel' else str(name).lower()

    def __module_exists(self, module_name):
        try:
            _module = importlib.import_module('models.' + module_name)
            return (True, _module)
        except (ModuleNotFoundError, AttributeError):
            return (False, None)

    def __save_instance(self, module, class_name, *args):
        entity = getattr(module, class_name)
        instance = entity(*args)
        instance.save()

    def __delete_instance(self, model, _id):
        key = '.'.join([model, _id])
        if self.storage.all().get(key, None) is None:
            print('** no instance found **')
            return
        self.storage.all().pop(key)


class HBNBCommand(cmd.Cmd):
    """A command-line parser for interactive use.

    This class provides a command-line interface for interactive use.
    Users can enter commands, and this parser interprets and processes
    those commands.

    Attributes:
        prompt (str): The command prompt to display.
    """
    prompt = '(hbnb) '
    bnbService = AirBnBService()

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        """Initialize the HBNBCommand.

        Args:
            completekey (str, optional): The key to trigger tab completion.
            Defaults to "tab".
            stdin (file, optional): The input stream to use. Defaults to None.
            stdout (file, optional): The output stream to use.
            Defaults to None.
        """
        super().__init__(completekey, stdin, stdout)

    def do_quit(self, args):
        """Quit command to exit the program"""
        sys.exit(0)

    def do_EOF(self, line):
        """Handle EOF (End of File).

        Args:
            line (str): The current line of input.

        Returns:
            bool: True to indicate the end of input.
        """
        return True

    def do_create(self, *args):
        _args = (str(args[0]).split(' '))
        if len(_args) < 1 or args[0] == '':
            print('** class name missing **')
            return

        if self.bnbService.create(_args[0]) is None:
            return

    def do_update(self, *args):
        _args = (str(args[0]).split(' '))
        _model, _attr, _id, _value = list([str()] * 4)
        try:
            _model = _args[0]
            _id = _args[1]
            _attr = _args[2]
            _value = _args[3]
        except (ValueError, IndexError):
            if _model is None or len(_model) == 0:
                print('** class name missing **')
                return
            if _id is None or len(_id) == 0:
                print('** instance id missing **')
                return
            if _attr is None or len(_attr) == 0:
                print('** attribute name missing **')
                return
            if _value is None or len(_value) == 0:
                print('** value missing **')
                return

        return self.bnbService.update_model_attribute(_model, _id,
                                                      _attr, _value)

    def do_destroy(self, *args):
        _args = (str(args[0]).split(' '))
        _model = ''
        _id = ''
        try:
            _model = _args[0]
            _id = _args[1]
        except (ValueError, IndexError):
            if len(_model) == 0:
                print('** class name missing **')
                return
            if _id is None or len(_id) == 0:
                print('** instance id missing **')
                return

        return self.bnbService.delete_model_by_id(_model, _id)

    def do_all(self, *args):
        return self.bnbService.fetch_all(args[0])

    def do_show(self, *args):
        _args = (str(args[0]).split(' '))
        _model = ''
        _id = ''
        try:
            _model = _args[0]
            _id = _args[1]
        except (ValueError, IndexError):
            if len(_model) == 0:
                print('** class name missing **')
                return
            if _id is None or len(_id) == 0:
                print('** instance id missing **')
                return

        if self.bnbService.fetch_model_by_id(_model, _id) is None:
            return

    def cmdloop(self, intro=None):
        super().cmdloop(intro)

    def process_args(self, argc, argv, isstdin=True):
        """Entrypoint for the command-line application

        This function serves as the entry point for the command-line
        application. It creates an instance of HBNBCommand and processes
        the provided arguments.

        Args:
            argc (int): The number of command-line arguments.
            argv (list): A list of command-line arguments.
            isstdin (bool, optional): Indicates whether input is from stdin.
            Defaults to True.

        Returns:
            None
        """
        import os

        argc, argv = len(sys.argv), sys.argv

        if not os.isatty(0):
            argv = sys.stdin.read().strip('\n')
            self.process_args(argc, argv, False)
            sys.exit(1)

        self.process_args(argc, argv)
        if not isstdin:
            self.onecmd(argv)
        else:
            self.cmdloop()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
