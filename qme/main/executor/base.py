"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.utils.file import read_file, get_user

import os
import tempfile
import uuid


class Capturing:
    """capture output from stdout and stderr into capture object.
       This is based off of github.com/vsoch/gridtest but modified
       to write files. The stderr and stdout are set to temporary files at
       the init of the capture, and then they are closed when we exit. This
       means expected usage looks like:

       with Capturing() as capture:
           process = subprocess.Popen(...)
           
       And then the output and error are retrieved from reading the files:
       and exposed as properties to the client:

           capture.out
           capture.err

       And cleanup means deleting these files, if they exist.
    """

    def __enter__(self):
        self.set_stdout()
        self.set_stderr()
        return self

    def set_stdout(self):
        self.stdout = open(tempfile.mkstemp()[1], "w")

    def set_stderr(self):
        self.stderr = open(tempfile.mkstemp()[1], "w")

    def __exit__(self, *args):
        self.stderr.close()
        self.stdout.close()

    @property
    def out(self):
        """Return output stream. Returns empty string if empty or doesn't exist.
           Returns (str) : output stream written to file
        """
        if os.path.exists(self.stdout.name):
            return read_file(self.stdout.name)
        return ""

    @property
    def err(self):
        """Return error stream. Returns empty string if empty or doesn't exist.
           Returns (str) : error stream written to file
        """
        if os.path.exists(self.stderr.name):
            return read_file(self.stderr.name)
        return ""

    def cleanup(self):
        for filename in [self.stdout.name, self.stderr.name]:
            if os.path.exists(filename):
                os.remove(filename)


class ExecutorBase:
    """A qme executor exists to translate a terminal command into a parsed
       job (shown in the dashboard) and expose one or more actions for it.
       The base executor will work for any generic command, generates
       status based on return codes, and exposes basic options to cancel (kill)
       or re-run.
    """

    name = "base"

    def __init__(self, taskid):
        """set a unique id that includes executor name (type) and random uuid)
        """
        uid = str(uuid.uuid4())
        if taskid:
            _, uid = taskid.split("-", 1)
        self.taskid = "%s-%s" % (self.name, uid)

    def _export_common(self):
        """export common task variables such as present working directory, user,
           This might include envars at some point, but we'd need to be careful.
        """
        return {"pwd": os.getcwd(), "user": get_user()}

    def export(self):
        """return data as json. This is intended to save to the task database.
           Any important output, returncode, etc. from the execute() function
           should be provided here. Required strings are "command" and "status"
           that must be one of "running" or "complete" or "cancelled." Suggested
           fields are output, error, and returncode. self._export_common() should
           be called first.
        """
        raise NotImplementedError

    def summary(self):
        return "[%s]" % self.name

    def execute(self, cmd):
        raise NotImplementedError

    def get_output(self):
        raise NotImplementedError

    def get_error(self):
        raise NotImplementedError
