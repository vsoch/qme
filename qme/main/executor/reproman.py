"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys
import re

from qme.utils.file import read_file
from qme.logger import bot
from .shell import ShellExecutor


class RepromanExecutor(ShellExecutor):
    """A reproman executor makes it easy to run commands on remote machines.
       This executor is not developed yet, but will implement a shell executor
       named reproman  for commands that start with reproman.
    """

    name = "reproman"
    matchstring = "^reproman"

    def __init__(self, taskid=None, command=None):
        super().__init__(taskid, command)

    def execute(self, cmd=None):
        """Execute a reproman command. If --list is used, the command is akin
           to a shell command and output is collected without further action.
        """
        self._execute(cmd)
