"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import locale
import os
import shlex
import shutil
import sys

from .base import ExecutorBase


class ShellExecutor(ExecutorBase):
    """A shell executor is the most basic of executors to run some shell command.
       We use the default functions provided by the BaseExecutor class to store
       the command, run, get the return code, and retry.
    """

    name = "shell"

    def __init__(self, taskid=None, command=None):
        self.reset(command)
        super().__init__(taskid)

    def summary(self):
        if self.returncode is not None:
            return "[%s][returncode: %s]" % (self.taskid, self.returncode)
        return "[%s][%s]" % (self.name, self.command)

    def reset(self, command=None):
        """refresh output and error streams
        """
        self.out = []
        self.err = []
        self.returncode = None
        self.pid = None
        self.cmd = []
        self.status = None
        if command:
            self.set_command(command)

    @property
    def command(self):
        return " ".join(self.cmd)

    def set_command(self, cmd):
        """parse is called when a new command is provided to ensure we have
           a list. We don't check that the executable is on the path,
           as the initialization might not occur in the runtime environment.
        """
        if not isinstance(cmd, list):
            cmd = shlex.split(cmd)
        self.cmd = cmd

    def execute(self, cmd=None):
        """Execute a system command and return output and error. Execute
           should take a cmd (a string or list) and execute it according to
           the executor. Attributes should be set on the class that are
           added to self.export. Since the functions here are likely needed
           by most executors, we create a self._execute() class that is called
           instead, and can be used by the other executors.
        """
        return self._execute(cmd)

    def _execute(self, cmd=None):
        """The actual class to do the execution - can be used if ShellExecutor
           is used as a super and the class using it defines a custom execute
        """
        # Reset the output and error records
        self.reset(cmd or self.cmd)

        # The executable must be found, return code 1 if not
        executable = shutil.which(self.cmd[0])
        if not executable:
            self.err = ["%s not found." % self.cmd[0]]
            self.returncode = 1
            return (self.out, self.err)

        # remove the original executable
        args = self.cmd[1:]
        self.status = "running"

        # Use updated command with executable and remainder (list)
        cmd = [executable] + args

        # Capturing provides temporary output and error files
        capture = self.capture(cmd)
        self.pid = capture.pid
        self.returncode = capture.returncode
        self.out = capture.output
        self.err = capture.error
        self.status = "complete"
        return (self.out, self.err)

    def export(self):
        """return data as json. This is intended to save to the task database.
           Any important output, returncode, etc. from the execute() function
           should be provided here. Required strings are "command" and "status"
           that must be one of "running" or "complete" or "cancelled." Suggested
           fields are output, error, and returncode. self._export_common() should
           be called first.
        """
        # Get common context (e.g., pwd)
        common = self._export_common()
        common.update(
            {
                "output": self.out,
                "error": self.err,
                "returncode": self.returncode,
                "command": self.cmd,
                "status": self.status,
                "pid": self.pid,
            }
        )
        return common

    def decode(self, line):
        """Given a line of output (error or regular) decode using the
           system default, if appropriate
        """
        loc = locale.getdefaultlocale()[1]

        try:
            line = line.decode(loc)
        except:
            pass
        return line

    def get_output(self):
        """Returns the output from shell command
        :rtype: str
        """
        return self.out

    def get_error(self):
        """Returns the error from shell command
        :rtype: str
        """
        return self.err
