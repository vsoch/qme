"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.main import Queue
import shlex
import sys


def run(args, extra):

    # Create a queue object, run the command to match to an executor
    queue = Queue(config_dir=args.config_dir)

    # Don't allow an empty command!
    if not args.cmd:
        sys.exit("Please provide a command for QueueMe to execute.")

    command = args.cmd

    # --help needs to be quoted, make sure if provided, gets parsed into command
    if any(["--help" in x for x in args.cmd]):
        command = []
        for item in args.cmd:
            command += shlex.split(item)

    # Extra might include unparsed arguments
    queue.run(command=command + extra, message=args.message)


def rerun(args, extra):

    # Create a queue object, run the command to match to an executor
    queue = Queue(config_dir=args.config_dir)
    queue.rerun(taskid=args.taskid, message=args.message)
