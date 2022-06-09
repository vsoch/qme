"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.exceptions import UnrecognizedExecutorError
from .shell import ShellExecutor
from .slurm import SlurmExecutor
import re


def matches(Executor, command):
    """Given a command, determine if it matches the regular expression
    that determines to use the executor or not. This applies to all
    executors except for the shell executor. This means that all non-shell
    classes need to have a matchstring defined.
    """
    if not hasattr(Executor, "matchstring"):
        raise NotImplementedError

    if isinstance(command, list):
        command = " ".join(command)
    return not re.search(Executor.matchstring, command) == None


def get_executor(command=None, config=None):
    """get executor will return the correct executor depending on a command (or
    other string) matching a regular expression. If nothing matches, we
    default to a shell executor. Each non-shell executor should expose
    a common "matches" function (provided by the base class) that will
    handle parsing the command (a list) to a single string, and checking
    if it matches a regular expression.
    """
    # Slurm Executor
    if matches(SlurmExecutor, command):
        executor = SlurmExecutor(command=command)

    # Default is standard shell command
    else:
        executor = ShellExecutor(command=command)
    executor.config = config
    return executor


def get_named_executor(name, taskid=None, config=None):
    """get a named executor, meaning determining based on name and not command"""
    if name == "shell":
        executor = ShellExecutor(taskid)
    elif name == "slurm":
        executor = SlurmExecutor(taskid)
    else:
        raise UnrecognizedExecutorError(name)
    executor.config = config
    return executor
