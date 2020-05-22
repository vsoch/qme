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


def test_executors_sqlite(tmp_path):
    """test each executor type with an sqlite database
    """
    from qme.main import Queue

    config_dir = os.path.join(str(tmp_path), ".qme")
    queue = Queue(config_dir=config_dir, database="sqlite")

    # The following commands should map to the following executors
    commands = ["ls"]
    executors = ["shell"]
    for i, command in enumerate(commands):

        # The executor name should be chosen based on the command
        name = executors[i]
        task = queue.run("ls")
        assert task.executor.name == name
        assert task.summary()

        # Task.load includes the file dump, the upper level keys should be same
        content = task.load()
        for key in ["executor", "uid", "data", "command"]:
            assert key in content

        # Task.export includes the executor specific data
        data = task.export()
        for key in ["pwd", "user", "timestamp"]:
            assert key in data


def test_relational(tmp_path):
    """Test loading and using a queue with the filesystem database.
    """
    from qme.main import Queue

    config_dir = os.path.join(str(tmp_path), ".qme")
    queue = Queue(config_dir=config_dir, database="sqlite")

    assert os.path.exists(config_dir)
    assert queue.config_dir == config_dir
    assert queue.config.configfile == os.path.join(queue.config_dir, "config.ini")
    assert queue.database == "sqlite"
    assert queue.db.database == "sqlite"

    # Test list, empty without anything
    assert not queue.list()

    # Run a task
    task = queue.run("ls")
    assert task.executor.name == "shell"
    assert task.taskid.startswith("shell")
    assert len(queue.list()) == 1

    # Rerun the task, should still only have one
    rerun = queue.rerun()
    assert rerun.taskid == task.taskid
    assert len(queue.list()) == 1

    # queue.get should return last task, given no id
    lasttask = queue.get()
    assert lasttask.taskid == task.taskid

    # Run a new task
    newtask = queue.run("whoami")
    assert len(queue.list()) == 2
    exports = newtask.export()

    # Search for tasks
    assert len(queue.search("ls")) > 0

    # Check exports
    for required in ["pwd", "output", "error", "cmd", "returncode"]:
        assert required in exports
    assert exports["pwd"] == os.getcwd()
    assert exports["cmd"] == ["whoami"]
    assert exports["returncode"] == 0

    # Get a task id that isn't the last task
    notlast = queue.get(task.taskid)
    assert task.taskid == notlast.taskid

    # Clean up a specific task (no prompt)
    queue.clear(task.taskid, noprompt=True)
    assert len(queue.list()) == 1
    queue.clear(noprompt=True)
    assert not queue.list()
