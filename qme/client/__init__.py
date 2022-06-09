#!/usr/bin/env python

"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.logger import QME_LOG_LEVEL, QME_LOG_LEVELS
import qme
import argparse
import sys
import logging


def get_parser():
    parser = argparse.ArgumentParser(description="QueueMe job executor and dashboard.")

    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--log_level",
        dest="log_level",
        choices=QME_LOG_LEVELS,
        default=QME_LOG_LEVEL,
        help="Customize logging level for QueueMe.",
    )

    parser.add_argument(
        "--config_dir",
        dest="config_dir",
        help="select database and configuration directory (defaults to $HOME/.qme).",
    )

    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="Add a message or description to store alongside a run.",
    )

    description = "actions for qme"
    subparsers = parser.add_subparsers(
        help="qme actions",
        title="actions",
        description=description,
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", help="show software version")

    # Configure qme (not written yet, will be written when databases added)
    config = subparsers.add_parser("config", help="configure qme")

    # Specify a database, if not sqlite must include a complete string
    config.add_argument(
        "--db",
        "--database",
        dest="database",
        default=None,
        help="select database backend for qme. [filesystem|sqlite] or [sqlite|mysql|postgresql]:///",
    )

    config.add_argument(
        "--set",
        help="set a setting, provide the executor, key, and value (set slurm sacct_format value)",
        default=None,
        dest="set",
        nargs=3,
    )

    # Clear an entire executor family, one task, or all tasks
    clear = subparsers.add_parser("clear", help="clear an executor, taskid, or target")
    clear.add_argument("target", nargs="?")
    clear.add_argument(
        "--force",
        dest="force",
        help="Don't ask for confirmation for delete (for headless).",
        default=False,
        action="store_true",
    )

    execute = subparsers.add_parser(
        "exec", help="execute an action for the last task, or a taskid"
    )
    execute.add_argument("actions", nargs="*")

    generate = subparsers.add_parser(
        "generate-key",
        help="generate a key for qme start, should be exported to QME_SERVER_KEY",
    )

    # List tasks and print to terminal
    ls = subparsers.add_parser("ls", help="list tasks")
    ls.add_argument(
        "executor", help="list one or more executors or taskids.", nargs="*"
    )

    # Run a command (gets passed to executor via template)
    run = subparsers.add_parser("run", help="run a command")
    run.add_argument(
        "cmd",
        nargs="*",
        help="The command to parse. If --help needed, should be fully quoted.",
    )

    # Rerun a task
    rerun = subparsers.add_parser("rerun", help="re-run a particular task")
    rerun.add_argument("taskid", nargs="?")

    # Start the queueMe dashboard
    search = subparsers.add_parser(
        "search",
        help="search for content in a command or metadata (sqlite or relational only)",
    )
    search.add_argument("query", nargs="*")

    # Start the queueMe dashboard
    start = subparsers.add_parser(
        "start", help="view the queue web interface (requires Flask)"
    )
    start.add_argument(
        "--port",
        dest="port",
        default=5000,
        type=int,
        help="select port to run qme dashboard on (defaults to 5000)",
    )
    start.add_argument(
        "--host",
        dest="host",
        default="127.0.0.1",
        type=str,
        help="the hostname to run for the server (defaults to 127.0.0.1)",
    )

    start.add_argument(
        "--debug",
        dest="debug",
        help="run server in debug mode (defaults to False)",
        default=False,
        action="store_true",
    )

    # Print complete metadata for a specific task
    get = subparsers.add_parser("get", help="get task")
    get.add_argument("taskid", help="list taskid to return", nargs="?")
    return parser


def main():
    """main entrypoint for qme"""

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

    # Set the logging level
    logging.basicConfig(level=getattr(logging, args.log_level))
    bot = logging.getLogger("qme.client")
    bot.setLevel(getattr(logging, args.log_level))

    # Show the version and exit
    if args.command == "version" or args.version:
        print(qme.__version__)
        sys.exit(0)

    # Does the user want a shell?
    if args.command == "clear":
        from .clear import main
    if args.command == "config":
        from .config import main
    if args.command == "exec":
        from .actions import main
    if args.command == "generate-key":
        from .generate import main
    if args.command == "get":
        from .get import main
    if args.command == "ls":
        from .listing import main
    if args.command == "run":
        from .run import run as main
    if args.command == "rerun":
        from .run import rerun as main
    if args.command == "search":
        from .search import main
    if args.command == "start":
        from .start import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, extra=extra)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
