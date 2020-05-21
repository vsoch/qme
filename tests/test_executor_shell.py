#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys
import pytest


def test_executor_shell(tmp_path):
    """Test the shell executor. A shell executor should have added a returncode,
       output, and error to it's data export.
    """
    from qme.main import Queue

    config_dir = os.path.join(str(tmp_path), ".qme")
    queue = Queue(config_dir=config_dir)
    task = queue.run("ls")
    assert task.executor.name == "shell"
    assert task.filename == os.path.join(
        queue.config_dir, "database", "shell", "%s.json" % task.taskid
    )
    assert task.summary()

    # Task.load includes the file dump, the upper level keys should be same
    content = task.load()
    for key in ["executor", "uid", "data"]:
        assert key in content

    # Task.export includes the executor specific data
    data = task.export()
    for key in ["cmd", "pwd", "output", "error", "returncode"]:
        assert key in data
