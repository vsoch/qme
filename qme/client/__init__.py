#!/usr/bin/env python

"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import qme
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="QueueMe job executor and dashboard.")

    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    description = "actions for qme"
    subparsers = parser.add_subparsers(
        help="qme actions", title="actions", description=description, dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", help="show software version")

    # Configure qme (not written yet, will be written when databases added)
    config = subparsers.add_parser("config", help="configure qme.")

    # TODO how to get password / credenitals? Setting here should BEGIN with these
    # and not be exposed as choices
    config.add_argument(
        "--db",
        "--database",
        dest="database",
        help="select database backend for qme.",
        choices=["filesystem", "sqlite", "mysql", "postgres"],
        default="filesystem",
    )

    # Run a command (gets passed to executor via template)
    run = subparsers.add_parser("run", help="Run a command to add to the queue.")
    run.add_argument("cmd", nargs="*")

    # List tasks and print to terminal
    ls = subparsers.add_parser("ls", help="List tasks")
    ls.add_argument(
        "executor", help="list one or more executors or taskids.", nargs="*"
    )

    # Print complete metadata for a specific task
    get = subparsers.add_parser("get", help="Get task")
    get.add_argument(
        "taskid", help="list taskid to return",
    )

    return parser


def main():
    """main entrypoint for qme
    """

    parser = get_parser()

    def help(return_code=0):
        """print help, including the software version and active client 
           and exit with return code.
        """
        version = qme.__version__

        print("\nQueueMe Python v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    # Show the version and exit
    if args.command == "version" or args.version:
        print(gridtest.__version__)
        sys.exit(0)

    # Does the user want a shell?
    if args.command == "config":
        from .config import main
    if args.command == "get":
        from .get import main
    if args.command == "ls":
        from .listing import main
    if args.command == "run":
        from .run import main

    # Pass on to the correct parser
    return_code = 0
    # try:
    main(args=args, extra=extra)
    #    sys.exit(return_code)
    # except UnboundLocalError:
    #    return_code = 1

    # help(return_code)


if __name__ == "__main__":
    main()
