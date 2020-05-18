"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.main import Queue
import sys
import os


def run(args, extra):

    # Create a queue object, run the command to match to an executor
    queue = Queue(config_dir=args.config_dir)

    # Don't allow an empty command!
    if not args.cmd:
        sys.exit("Please provide a command for QueueMe to execute.")
    queue.run(args.cmd)


def rerun(args, extra):

    # Create a queue object, run the command to match to an executor
    queue = Queue(config_dir=args.config_dir)
    queue.rerun(args.taskid)
