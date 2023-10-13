#!/usr/bin/env python3

"""
console.py - Entrypoint for AirBnB CLI application

This module provides the main entrypoint for the program. It
parses and handles the commands.

Classes:
    HBNBCommand: A command-line parser class.
"""

import importlib
import sys
import cmd

from models.engine.file_storage import FileStorage


class AirBnBService:

    storage = FileStorage()

    def create(self, *args):
        class_name = str(args[0][0])
        _module_name = 'base_model' if args[0][0] == 'BaseModel' else str(
            args[0][0]).lower()
        try:
            _module = importlib.import_module('models.'+_module_name)
            entity = getattr(_module, class_name)
            instance = entity(*args)
            self.storage.new(instance)
        except (ModuleNotFoundError, AttributeError):
            print("** class doesn't exist **")
            return None

    def save(self):
        pass

    def destroy(self):
        pass

    def fetch_all(self, model, id):
        pass

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
        if len(args) < 1 or args[0] == '':
            print('** class name missing **')
            return

        if self.bnbService.create(args) is None:
            return

    def do_update(self, *args):
        pass

    def do_destroy(self, *args):
        pass

    def do_all(self, *args):
        pass

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
        
        if self.bnbService.fetch_all(_model, _id) is None:
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
