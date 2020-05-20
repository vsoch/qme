"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .shell import ShellExecutor
from .slurm import SlurmExecutor
import sys
import re


def get_executor(command=None):
    """get executor will return the correct executor depending on a command (or
       other string) matching a regular expression. Currently we just have a 
       ShellExecutor.
    """
    # Command needs to be joined into single string for regular expression
    cmd = " ".join(command)

    # Slurm Executor
    if re.search(cmd, "srun"):
        return SlurmExecutor(command=command)

    # Default is standard shell command
    return ShellExecutor(command=command)


def get_named_executor(name, taskid=None):
    """get a named executor, meaning determining based on name and not command
    """
    if name == "shell":
        return ShellExecutor(taskid)
    sys.exit(f"{name} is not a known executor.")
