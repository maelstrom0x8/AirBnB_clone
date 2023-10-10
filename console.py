#!/usr/bin/env python3

import sys
import cmd


class CommandLineParser(cmd.Cmd):
    prompt = '(hbnb) '

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)

    def do_quit(self, args):
        "Exit the program"
        sys.exit(0)
    
    def do_EOF(self, line):
        """Handle EOF"""
        return True


def main(argc, argv, ioflag=True):
    """Entrypoint"""
    parser = CommandLineParser()
    if not ioflag:
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
