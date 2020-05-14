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
import subprocess
import sys

from .base import ExecutorBase, Capturing


class ShellExecutor(ExecutorBase):
    """A shell executor is the most basic of executors to run some shell command.
       We use the default functions provided by the BaseExecutor class to store
       the command, run, get the return code, and retry.
    """

    name = "shell"

    def __init__(self, taskid=None):
        self.reset()
        super().__init__(taskid)

    def summary(self):
        if self.returncode is not None:
            return "[%s][returncode: %s]" % (self.taskid, self.returncode,)
        return "[%s][%s]" % (self.name, self.command)

    def reset(self):
        """refresh output and error streams
        """
        self.out = []
        self.err = []
        self.returncode = None
        self.cmd = []

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

    def execute(self, cmd):
        """Execute a system command and return output and error.
        """
        # Reset the output and error records
        self.reset()
        self.set_command(cmd)

        # The executable must be found, return code 1 if not
        executable = shutil.which(self.cmd[0])
        if not executable:
            self.err = ["%s not found." % self.cmd[0]]
            self.returncode = 1
            return (self.out, self.err)

        # remove the original executable
        args = self.cmd[1:]

        # Use updated command with executable and remainder (list)
        cmd = [executable] + args

        # Capturing provides temporary output and error files
        with Capturing() as capture:
            process = subprocess.Popen(
                cmd,
                stdout=capture.stdout,
                stderr=capture.stderr,
                universal_newlines=True,
            )
            returncode = process.poll()

            # Iterate through the output
            while returncode is None:
                returncode = process.poll()

        # Get the remainder of lines, add return code
        self.out += [x for x in self.decode(capture.out) if x]
        self.err += [x for x in self.decode(capture.err) if x]

        # Cleanup capture files and save final return code
        capture.cleanup()
        self.returncode = returncode
        return (self.out, self.err)

    def export(self):
        """return data as json. This is intended to save to the task database
        """
        return {"output": self.out, "error": self.err, "returncode": self.returncode}

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
