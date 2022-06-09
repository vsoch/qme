"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.main import Queue


def main(args, extra):

    # Clear an executor, taskid, or target
    queue = Queue(config_dir=args.config_dir)
    queue.clear(args.target, noprompt=args.force)
