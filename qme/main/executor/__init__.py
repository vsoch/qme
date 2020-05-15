"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .shell import ShellExecutor
import sys


def get_executor(command=None):
    """get executor will return the correct executor depending on a command (or
       other string) matching a regular expression. Currently we just have a 
       ShellExecutor.
    """
    # TODO: each executor should have a regular expression to match command.
    return ShellExecutor()


def get_named_executor(name, taskid=None):
    """get a named executor, meaning determining based on name and not command
    """
    if name == "shell":
        return ShellExecutor(taskid)
    sys.exit(f"{name} is not a known executor.")
