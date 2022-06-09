"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.main import Queue
import sys


def main(args, extra):

    # Create a queue object, run the command to match to an executor
    queue = Queue(config_dir=args.config_dir)

    # Pass the queue object to start a server
    try:
        from qme.app.server import start

        start(port=args.port, queue=queue, debug=args.debug, level=args.log_level)
    except ModuleNotFoundError:
        sys.exit(
            "You must 'pip install qme[app]' 'pip install qme[all]' to use the dashboard."
        )
