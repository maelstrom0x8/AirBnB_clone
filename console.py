#!/usr/bin/env python3

import sys
import cmd


class CommandLineParser(cmd.Cmd):
    """A command-line parser for interactive use.

    This class provides a command-line interface for interactive use. Users can
    enter commands, and this parser interprets and processes those commands.

    Attributes:
        prompt (str): The command prompt to display.
    """
    prompt = '(hbnb) '

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        """Initialize the CommandLineParser.

        Args:
            completekey (str, optional): The key to trigger tab completion. Defaults to "tab".
            stdin (file, optional): The input stream to use. Defaults to None.
            stdout (file, optional): The output stream to use. Defaults to None.
        """
        super().__init__(completekey, stdin, stdout)

    def do_quit(self, args):
        """Quit the program.

        Args:
            args (str): Additional arguments (ignored).

        Returns:
            None
        """
        sys.exit(0)
    
    def do_EOF(self, line):
        """Handle EOF (End of File).

        Args:
            line (str): The current line of input.

        Returns:
            bool: True to indicate the end of input.
        """
        return True


def main(argc, argv, isstdin=True):
    """Entrypoint for the command-line application

    This function serves as the entry point for the command-line application. It creates
    an instance of CommandLineParser and processes the provided arguments.

    Args:
        argc (int): The number of command-line arguments.
        argv (list): A list of command-line arguments.
        isstdin (bool, optional): Indicates whether input is from stdin. Defaults to True.

    Returns:
        None
    """
    parser = CommandLineParser()
    if not isstdin:
        parser.onecmd(argv)
    else:
        parser.cmdloop()


if __name__ == '__main__':
    import os

    argc, argv = len(sys.argv), sys.argv

    if not os.isatty(0):
        argv = sys.stdin.read().strip('\n')
        main(argc, argv, False)
        sys.exit(1)

    main(argc, argv)
