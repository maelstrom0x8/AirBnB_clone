#!/usr/bin/env python3

"""
console.py - Entrypoint for AirBnB CLI application

This module provides the main entrypoint for the program. It
parses and handles the commands.

Classes:
    HBNBService: A service class to manage creation, updates, and
    deletions of entities.
    HBNBCommand: A command-line parser class for interactive use.
"""

import cmd
import importlib
import os
import re
import sys
from datetime import datetime

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBService:
    """
    A service class to manage creation, updates, and deletions of entities.
    """

    storage = FileStorage()

    def create(self, args):
        """
        Create a new model.

        Args:
            args (str): The entity's class name.
        """
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
        """
        Update model data.

        Args:
            model (str): The entity's class name.
            id (str): The entity's ID.
            attr (str): The attribute to update.
            value (str): The new value for the attribute.
        """
        _module_name = self.__get_module(model)
        b, _ = self.__module_exists(_module_name)
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
        """
        Remove a model by its ID.

        Args:
            model (str): The entity's class name.
            _id (str): The entity's ID.
        """
        _module_name = self.__get_module(model)
        b, _ = self.__module_exists(_module_name)
        if not b:
            print("** class doesn't exist **")
            return
        else:
            self.__delete_instance(model, _id)

    def fetch_model_by_id(self, model, id):
        """
        Print a model instance.

        Args:
            model (str): The entity's class name.
            id (str): The entity's ID.
        """
        module_name = self.__get_module(model)
        b, module = self.__module_exists(module_name)
        if b:
            entity = getattr(module, model)
            if entity is None:
                print("** class doesn't exist **")
                return
        else:
            print("** class doesn't exist **")
            return
        key = '.'.join([model, id])
        _model = self.storage.all().get(key, None)
        if _model is None:
            print('** instance not found **')
            return
        print(_model)

    def fetch_all(self, model):
        """
        Lists all models of a class.

        Args:
            model (str): The entity's class name.
        """
        module_name = self.__get_module(model)
        b, module = self.__module_exists(module_name)
        if b:
            entity = getattr(module, model)
            if entity is None:
                print("** class doesn't exist **")
                return
        else:
            print("** class doesn't exist **")
            return
        _models = self.storage.all()
        for e in _models.values():
            if e.__class__.__name__ == model:
                print(e)
        return

    def fetch_model_count(self, model):
        """
        Prints the number of entities of a class.

        Args:
            model (str): The entity's class name.
        """
        module_name = self.__get_module(model)
        b, module = self.__module_exists(module_name)
        if b:
            entity = getattr(module, model)
            if entity is None:
                print("** class doesn't exist **")
                return
        else:
            print("** class doesn't exist **")
            return
        _models = [x for x in self.storage.all().values()
                   if x.__class__.__name__ == model]
        print(len(_models))
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
        print(instance.id)
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
    bnbService = HBNBService()

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
        """Exit the program"""
        sys.exit(0)

    def do_EOF(self, line):
        """Handle EOF"""
        return True

    def do_create(self, *args):
        """Create a new model"""
        _args = (str(args[0]).split(' '))
        if len(_args) < 1 or args[0] == '':
            print('** class name missing **')
            return

        if self.bnbService.create(_args[0]) is None:
            return

    def do_update(self, *args):
        """Update model data"""
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
        """Remove a model by id"""
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
        """Lists all models of a class"""
        _args = args[0].split(' ')
        return self.bnbService.fetch_all(_args[0])

    def do_count(self, *args):
        """Prints the number of a model class"""
        _args = args[0].split(' ')
        if len(_args) < 1:
            print('** class name missing **')

        return self.bnbService.fetch_model_count(_args[0])

    def do_show(self, *args):
        """Prints a model instance"""
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

    def emptyline(self) -> bool:
        return False

    def preloop(self) -> None:
        if not os.isatty(0):
            self.prompt = ''
            self.onecmd('')

    def precmd(self, line: str):
        try:
            _fn = 'do_' + line.split(' ')[0]
            if getattr(self, _fn) is not None:
                return super().precmd(line)
        except (AttributeError):
            try:
                ln = self.preprocess_input(line)
                return super().precmd(ln)
            except (AttributeError, TypeError, ValueError, IndexError):
                return super().precmd(line)

        return super().precmd(line)

    def preprocess_input(self, line: str):
        args = [self.remove_quotes(x)
                for x in self.tokenize_string(line)]
        _entity = args[0]
        _method = args[1]
        _args = args[2:]
        if getattr(self, 'do_' + _method) is not None:
            return ' '.join([_method, _entity] + _args)

    def remove_quotes(self, input: str):
        if input.startswith(('"', "'")) and input.endswith(('"', "'")):
            return input[1:-1]
        else:
            return input

    def tokenize_string(self, input_string):
        if input_string is None or len(input_string) == 0:
            return ['']
        pattern = r'([A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*)\.([A \
        -Za-z_][A-Za-z0-9_]*)\(([^)]*)\)'

        match = re.match(pattern, input_string)
        if match:
            class_name = match.group(1)
            method_name = match.group(3)
            args = [arg.strip() for arg in match.group(4).split(',')]
            return [class_name, method_name] + args

        return None


if __name__ == '__main__':
    HBNBCommand().cmdloop()
