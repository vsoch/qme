"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.main import Queue
from qme.main.executor import get_named_executor
from qme.logger import bot
import sys


def main(args, extra):

    result = None
    if not args.actions:
        sys.exit("Please provide an executor to list actions for, or an action.")

    # User has provided an executor to list actions for
    elif len(args.actions) == 1:

        # Assume looking for executor first, fall back to action on last job
        try:
            executor = get_named_executor(args.actions[0])
            actions = [[x] for x in executor.get_actions()]
            bot.table(actions)
        except:
            queue = Queue(config_dir=args.config_dir)
            task = queue.get()
            result = task.run_action(args.actions[0])

    # NEED TO DEBUG THIS FOR SLURM
    # user provided exec <action> <taskid>
    elif len(args.actions) == 2:
        taskid, action = args.actions
        queue = Queue(config_dir=args.config_dir)
        task = queue.get(taskid)
        result = task.run_action(action)

    # Print result to terminal
    if result:
        if isinstance(result, list):
            result = " ".join(result)
        print(result)
