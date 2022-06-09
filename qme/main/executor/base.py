"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.utils.file import read_file, get_user

from datetime import datetime
import os
import tempfile
import subprocess
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
        self.output = []
        self.error = []
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
        """set a unique id that includes executor name (type) and random uuid)"""
        uid = str(uuid.uuid4())
        if taskid:
            _, uid = taskid.split("-", 1)
        self.taskid = "%s-%s" % (self.name, uid)
        self.pwd = os.getcwd()
        self.message = None
        self.actions = {}
        if not hasattr(self, "data"):
            self.data = {}

    def _export_common(self):
        """export common task variables such as present working directory, user,
        and timestamp for when it was run. This might include envars at some
        point, but we'd need to be careful.
        """
        common = {
            "pwd": self.pwd,
            "user": get_user(),
            "timestamp": str(datetime.now()),
        }
        if self.message:
            common["message"] = self.message
        return common

    def export(self):
        """return data as json. This is intended to save to the task database.
        Any important executor specific metadata should be added to self.data
        """
        # Get common context (e.g., pwd)
        common = self._export_common()
        common.update(self.data)
        return common

    @property
    def command(self):
        raise NotImplementedError

    def run_action(self, name, data, **kwargs):
        """Check for a named action in the executors list.
        This is called from the queue that can also add the data for the task
        as "data." The user should be able to run an action by name, e.g.,
        executor.action('status', data) and take key word arguments, which
        is exposed by a task as task.run_action('status', data)
        """
        if name in self.actions:
            return self.actions[name](data, **kwargs)

    def get_actions(self):
        """return list of actions to expose"""
        return list(self.actions)

    def capture(self, cmd):
        """capture is a helper function to capture a shell command. We
        use Capturing and then save attributes like the pid, output, error
        to it, and return to the calling function. For example:

        capture = self.capture_command(cmd)
        self.pid = capture.pid
        self.returncode = capture.returncode
        self.out = capture.output
        self.err = capture.error
        """
        # Capturing provides temporary output and error files
        with Capturing() as capture:
            process = subprocess.Popen(
                cmd,
                stdout=capture.stdout,
                stderr=capture.stderr,
                universal_newlines=True,
            )
            capture.pid = process.pid
            returncode = process.poll()

            # Iterate through the output
            while returncode is None:
                returncode = process.poll()

        # Get the remainder of lines, add return code
        capture.output += [x for x in self.decode(capture.out) if x]
        capture.error += [x for x in self.decode(capture.err) if x]

        # Cleanup capture files and save final return code
        capture.cleanup()
        capture.returncode = returncode
        return capture

    def get_setting(self, key, default=None):
        """Get a setting, meaning that we first check the environment, then
        the config file, and then (if provided) a default.
        """
        # First preference to environment
        envar = ("QME_%s_%s" % (self.name, key)).upper()
        envar = os.environ.get(envar)
        if envar is not None:
            return envar

        # Next preference to config setting
        executor = "executor.%s" % self.name
        if executor not in self.config.config:
            return default
        if key in self.config.config[executor]:
            return self.config.get(executor, key)
        return default

    def summary(self):
        return "[%s]" % self.name

    def execute(self, cmd=None, message=None):
        raise NotImplementedError

    def get_output(self):
        raise NotImplementedError

    def get_error(self):
        raise NotImplementedError
